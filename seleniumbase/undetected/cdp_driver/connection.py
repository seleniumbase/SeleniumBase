from __future__ import annotations
import asyncio
import collections
import inspect
import itertools
import json
import logging
import sys
import types
from asyncio import iscoroutine, iscoroutinefunction
from typing import (
    Optional,
    Generator,
    Union,
    Awaitable,
    Callable,
    Any,
    TypeVar,
)
import websockets
from websockets.protocol import State
from . import cdp_util as util
import mycdp as cdp
import mycdp.network
import mycdp.page
import mycdp.storage
import mycdp.runtime
import mycdp.target
import mycdp.util

T = TypeVar("T")
GLOBAL_DELAY = 0.005
MAX_SIZE: int = 2**28
PING_TIMEOUT: int = 1800  # 30 minutes
TargetType = Union[cdp.target.TargetInfo, cdp.target.TargetID]
logger = logging.getLogger("uc.connection")


class ProtocolException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = None
        self.code = None
        self.args = args
        if isinstance(args[0], dict):
            self.message = args[0].get("message", None)  # noqa
            self.code = args[0].get("code", None)
        elif hasattr(args[0], "to_json"):
            def serialize(obj, _d=0):
                res = "\n"
                for k, v in obj.items():
                    space = "\t" * _d
                    if isinstance(v, dict):
                        res += f"{space}{k}: {serialize(v, _d + 1)}\n"
                    else:
                        res += f"{space}{k}: {v}\n"
                return res
            self.message = serialize(args[0].to_json())
        else:
            self.message = "| ".join(str(x) for x in args)

    def __str__(self):
        return f"{self.message} [code: {self.code}]" if self.code else f"{self.message}"  # noqa


class SettingClassVarNotAllowedException(PermissionError):
    pass


class Transaction(asyncio.Future):
    __cdp_obj__: Generator = None
    method: str = None
    params: dict = None
    id: int = None

    def __init__(self, cdp_obj: Generator):
        """
        :param cdp_obj:
        """
        super().__init__()
        self.__cdp_obj__ = cdp_obj
        self.connection = None
        self.method, *params = next(self.__cdp_obj__).values()
        if params:
            params = params.pop()
        self.params = params

    @property
    def message(self):
        return json.dumps(
            {"method": self.method, "params": self.params, "id": self.id}
        )

    @property
    def has_exception(self):
        try:
            if self.exception():
                return True
        except BaseException:
            return True
        return False

    def __call__(self, **response: dict):
        """
        Parses the response message and marks the future complete.
        :param response:
        """
        if "error" in response:
            # Set exception and bail out
            return self.set_exception(ProtocolException(response["error"]))
        try:
            # Try to parse the result according to the PyCDP docs.
            self.__cdp_obj__.send(response["result"])
        except StopIteration as e:
            # Exception value holds the parsed response
            return self.set_result(e.value)
        raise ProtocolException(
            "Could not parse the cdp response:\n%s" % response
        )

    def __repr__(self):
        success = False if (self.done() and self.has_exception) else True
        if self.done():
            status = "finished"
        else:
            status = "pending"
        fmt = (
            f"<{self.__class__.__name__}\n\t"
            f"method: {self.method}\n\t"
            f"status: {status}\n\t"
            f"success: {success}>"
        )
        return fmt


class EventTransaction(Transaction):
    event = None
    value = None

    def __init__(self, event_object):
        try:
            super().__init__(None)
        except BaseException:
            pass
        self.set_result(event_object)
        self.event = self.value = self.result()

    def __repr__(self):
        status = "finished"
        success = False if self.exception() else True
        event_object = self.result()
        fmt = (
            f"{self.__class__.__name__}\n\t"
            f"event: {event_object.__class__.__module__}.{event_object.__class__.__name__}\n\t"  # noqa
            f"status: {status}\n\t"
            f"success: {success}>"
        )
        return fmt


class CantTouchThis(type):
    def __setattr__(cls, attr, value):
        """:meta private:"""
        if attr == "__annotations__":
            # Fix autodoc
            return super().__setattr__(attr, value)
        raise SettingClassVarNotAllowedException(
            "\n".join(
                (
                    "don't set '%s' on the %s class directly, "
                    "as those are shared with other objects.",
                    "use `my_object.%s = %s`  instead",
                )
            )
            % (attr, cls.__name__, attr, value)
        )


class Connection(metaclass=CantTouchThis):
    attached: bool = None
    websocket: websockets.WebSocketClientProtocol
    _target: cdp.target.TargetInfo

    def __init__(
        self,
        websocket_url=None,
        target=None,
        _owner=None,
        **kwargs,
    ):
        super().__init__()
        self._target = target
        self.__count__ = itertools.count(0)
        self._owner = _owner
        self.websocket_url: str = websocket_url
        self.websocket = None
        self.mapper = {}
        self.handlers = collections.defaultdict(list)
        self.recv_task = None
        self.enabled_domains = []
        self._last_result = []
        self.listener: Listener = None
        self.__dict__.update(**kwargs)

    @property
    def target(self) -> cdp.target.TargetInfo:
        return self._target

    @target.setter
    def target(self, target: cdp.target.TargetInfo):
        if not isinstance(target, cdp.target.TargetInfo):
            raise TypeError(
                "target must be set to a '%s' but got '%s"
                % (cdp.target.TargetInfo.__name__, type(target).__name__)
            )
        self._target = target

    @property
    def closed(self):
        if not self.websocket:
            return True
        return self.websocket.closed

    def add_handler(
        self,
        event_type_or_domain: Union[type, types.ModuleType],
        handler: Union[Callable, Awaitable],
    ):
        """
        Add a handler for given event.
        If event_type_or_domain is a module instead of a type,
        it will find all available events and add the handler.
        If you want to receive event updates (eg. network traffic),
        you can add handlers for those events.
        Handlers can be regular callback functions
        or async coroutine functions (and also just lambdas).
        For example, if you want to check the network traffic:
        .. code-block::
            page.add_handler(
                cdp.network.RequestWillBeSent, lambda event: print(
                    'network event => %s' % event.request
                )
            )
        Next time there's network traffic, you'll see lots of console output.
        :param event_type_or_domain:
        :param handler:
        """
        if isinstance(event_type_or_domain, types.ModuleType):
            for name, obj in inspect.getmembers_static(event_type_or_domain):
                if name.isupper():
                    continue
                if not name[0].isupper():
                    continue
                if not isinstance(obj, type):
                    continue
                if inspect.isbuiltin(obj):
                    continue
                self.handlers[obj].append(handler)
            return
        self.handlers[event_type_or_domain].append(handler)

    async def aopen(self, **kw):
        """
        Opens the websocket connection. Shouldn't be called manually by users.
        """
        if not self.websocket or self.websocket.state is State.CLOSED:
            try:
                self.websocket = await websockets.connect(
                    self.websocket_url,
                    ping_timeout=PING_TIMEOUT,
                    max_size=MAX_SIZE,
                )
                self.listener = Listener(self)
            except (Exception,) as e:
                logger.debug("Exception during opening of websocket: %s", e)
                if self.listener:
                    self.listener.cancel()
                raise
        if not self.listener or not self.listener.running:
            self.listener = Listener(self)
            logger.debug(
                "\n✅ Opened websocket connection to %s", self.websocket_url
            )
        # When a websocket connection is closed (either by error or on purpose)
        # and reconnected, the registered event listeners (if any), should be
        # registered again, so the browser sends those events.
        await self._register_handlers()

    async def aclose(self):
        """
        Closes the websocket connection. Shouldn't be called manually by users.
        """
        if self.websocket and self.websocket.state is not State.CLOSED:
            if self.listener and self.listener.running:
                self.listener.cancel()
                self.enabled_domains.clear()
            await asyncio.sleep(0.015)
            try:
                await self.websocket.close()
            except Exception:
                logger.debug(
                    "\n❌ Error closing websocket connection to %s",
                    self.websocket_url
                )
            logger.debug(
                "\n❌ Closed websocket connection to %s", self.websocket_url
            )

    async def sleep(self, t: Union[int, float] = 0.25):
        await self.update_target()
        await asyncio.sleep(t)

    def feed_cdp(self, cdp_obj):
        """
        Used in specific cases, mostly during cdp.fetch.RequestPaused events,
        in which the browser literally blocks.
        By using feed_cdp, you can issue a response without a blocking "await".
        Note: This method won't cause a response.
        Note: This is not an async method, just a regular method!
        :param cdp_obj:
        """
        asyncio.ensure_future(self.send(cdp_obj))

    async def wait(self, t: Union[int, float] = None):
        """
        Waits until the event listener reports idle
        (no new events received in certain timespan).
        When `t` is provided, ensures waiting for `t` seconds, no matter what.
        :param t:
        """
        await self.update_target()
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        try:
            if isinstance(t, (int, float)):
                await asyncio.wait_for(self.listener.idle.wait(), timeout=t)
                while (loop.time() - start_time) < t:
                    await asyncio.sleep(0.1)
            else:
                await self.listener.idle.wait()
        except asyncio.TimeoutError:
            if isinstance(t, (int, float)):
                # Explicit time is given, which is now passed, so leave now.
                return
        except AttributeError:
            # No listener created yet.
            pass

    async def set_locale(self, locale: Optional[str] = None):
        """Sets the Language Locale code via set_user_agent_override."""
        await self.send(cdp.network.set_user_agent_override("", locale))

    def __getattr__(self, item):
        """:meta private:"""
        try:
            return getattr(self.target, item)
        except AttributeError:
            raise

    async def __aenter__(self):
        """:meta private:"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """:meta private:"""
        await self.aclose()
        if exc_type and exc_val:
            raise exc_type(exc_val)

    def __await__(self):
        """
        Updates targets and wait for event listener to report idle.
        Idle is reported when no new events are received for 1 second.
        """
        return self.wait().__await__()

    async def update_target(self):
        target_info: cdp.target.TargetInfo = await self.send(
            cdp.target.get_target_info(self.target_id), _is_update=True
        )
        self.target = target_info

    async def send(
        self,
        cdp_obj: Generator[dict[str, Any], dict[str, Any], Any],
        _is_update=False,
    ) -> Any:
        """
        Send a protocol command.
        The commands are made using any of the cdp.<domain>.<method>()'s
        and is used to send custom cdp commands as well.
        :param cdp_obj: The generator object created by a cdp method
        :param _is_update: Internal flag
            Prevents infinite loop by skipping the registeration of handlers
            when multiple calls to connection.send() are made.
        """
        await self.aopen()
        if not self.websocket or self.websocket.state is State.CLOSED:
            return
        if self._owner:
            browser = self._owner
            if browser.config:
                if browser.config.expert:
                    await self._prepare_expert()
                if browser.config.headless:
                    await self._prepare_headless()
        if not self.listener or not self.listener.running:
            self.listener = Listener(self)
        try:
            tx = Transaction(cdp_obj)
            tx.connection = self
            if not self.mapper:
                self.__count__ = itertools.count(0)
            tx.id = next(self.__count__)
            self.mapper.update({tx.id: tx})
            if not _is_update:
                await self._register_handlers()
            await self.websocket.send(tx.message)
            try:
                return await tx
            except ProtocolException as e:
                e.message += f"\ncommand:{tx.method}\nparams:{tx.params}"
                raise e
        except Exception:
            await self.aclose()

    async def _register_handlers(self):
        """
        Ensure that for current (event) handlers, the corresponding
        domain is enabled in the protocol.
        """
        # Save a copy of current enabled domains in a variable.
        # At the end, this variable will hold the domains that
        # are not represented by handlers, and can be removed.
        enabled_domains = self.enabled_domains.copy()
        for event_type in self.handlers.copy():
            domain_mod = None
            if len(self.handlers[event_type]) == 0:
                self.handlers.pop(event_type)
                continue
            if isinstance(event_type, type):
                domain_mod = util.cdp_get_module(event_type.__module__)
            if domain_mod in self.enabled_domains:
                # At this point, the domain is being used by a handler, so
                # remove that domain from temp variable 'enabled_domains'.
                if domain_mod in enabled_domains:
                    enabled_domains.remove(domain_mod)
                continue
            elif domain_mod not in self.enabled_domains:
                if domain_mod in (cdp.target, cdp.storage):
                    continue
                try:
                    # Prevent infinite loops.
                    logger.debug("Registered %s", domain_mod)
                    self.enabled_domains.append(domain_mod)
                    await self.send(domain_mod.enable(), _is_update=True)
                except BaseException:  # Don't error before request is sent
                    logger.debug("", exc_info=True)
                    try:
                        self.enabled_domains.remove(domain_mod)
                    except BaseException:
                        logger.debug("NOT GOOD", exc_info=True)
                        continue
                finally:
                    continue
        for ed in enabled_domains:
            # Items still present at this point are unused and need removal.
            self.enabled_domains.remove(ed)

    async def _prepare_headless(self):
        return  # (This functionality has moved to a new location!)

    async def _prepare_expert(self):
        if getattr(self, "_prep_expert_done", None):
            return
        if self._owner:
            part1 = "Element.prototype._attachShadow = "
            part2 = "Element.prototype.attachShadow"
            parts = part1 + part2
            await self._send_oneshot(
                cdp.page.add_script_to_evaluate_on_new_document(
                    """
                    %s;
                    Element.prototype.attachShadow = function () {
                        return this._attachShadow( { mode: "open" } );
                    };
                    """ % parts
                )
            )
            await self._send_oneshot(cdp.page.enable())
        setattr(self, "_prep_expert_done", True)

    async def _send_oneshot(self, cdp_obj):
        tx = Transaction(cdp_obj)
        tx.connection = self
        tx.id = -2
        self.mapper.update({tx.id: tx})
        await self.websocket.send(tx.message)
        try:
            # In try/except since if browser connection sends this,
            # then it raises an exception.
            return await tx
        except ProtocolException:
            pass


class Listener:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.history = collections.deque()
        self.max_history = 1000
        self.task: asyncio.Future = None
        is_interactive = getattr(sys, "ps1", sys.flags.interactive)
        self._time_before_considered_idle = 0.10 if not is_interactive else 0.75  # noqa
        self.idle = asyncio.Event()
        self.run()

    def run(self):
        self.task = asyncio.create_task(self.listener_loop())

    @property
    def time_before_considered_idle(self):
        return self._time_before_considered_idle

    @time_before_considered_idle.setter
    def time_before_considered_idle(self, seconds: Union[int, float]):
        self._time_before_considered_idle = seconds

    def cancel(self):
        if self.task and not self.task.cancelled():
            self.task.cancel()

    @property
    def running(self):
        if not self.task:
            return False
        if self.task.done():
            return False
        return True

    async def listener_loop(self):
        while True:
            try:
                msg = await asyncio.wait_for(
                    self.connection.websocket.recv(),
                    self.time_before_considered_idle,
                )
            except asyncio.TimeoutError:
                self.idle.set()
                # Pause for a moment.
                # await asyncio.sleep(self.time_before_considered_idle / 10)
                await asyncio.sleep(0.015)
                continue
            except (Exception,) as e:
                logger.debug(
                    "Connection listener exception "
                    "while reading websocket:\n%s", e
                )
                break
            if not self.running:
                # If we have been cancelled or otherwise stopped running,
                # then break this loop.
                break
            self.idle.clear()  # Not "idle" anymore.
            message = json.loads(msg)
            if "id" in message:
                if message["id"] in self.connection.mapper:
                    tx = self.connection.mapper.pop(message["id"])
                    logger.debug(
                        "Got answer for %s (message_id:%d)", tx, message["id"]
                    )
                    tx(**message)
                else:
                    if message["id"] == -2:
                        tx = self.connection.mapper.get(-2)
                        if tx:
                            tx(**message)
                        continue
            else:
                # Probably an event
                try:
                    event = cdp.util.parse_json_event(message)
                    event_tx = EventTransaction(event)
                    if not self.connection.mapper:
                        self.connection.__count__ = itertools.count(0)
                    event_tx.id = next(self.connection.__count__)
                    self.connection.mapper[event_tx.id] = event_tx
                except Exception as e:
                    logger.info(
                        "%s: %s during parsing of json from event : %s"
                        % (type(e).__name__, e.args, message),
                        exc_info=True,
                    )
                    continue
                except KeyError as e:
                    logger.info("KeyError: %s" % e, exc_info=True)
                    continue
                try:
                    if type(event) in self.connection.handlers:
                        callbacks = self.connection.handlers[type(event)]
                    else:
                        continue
                    if not len(callbacks):
                        continue
                    for callback in callbacks:
                        try:
                            if (
                                iscoroutinefunction(callback)
                                or iscoroutine(callback)
                            ):
                                try:
                                    await callback(event, self.connection)
                                except TypeError:
                                    await callback(event)
                            else:
                                try:
                                    callback(event, self.connection)
                                except TypeError:
                                    callback(event)
                        except Exception as e:
                            logger.warning(
                                "Exception in callback %s for event %s => %s",
                                callback,
                                event.__class__.__name__,
                                e,
                                exc_info=True,
                            )
                            raise
                except asyncio.CancelledError:
                    break
                except Exception:
                    raise
                continue

    def __repr__(self):
        s_idle = "[idle]" if self.idle.is_set() else "[busy]"
        s_cache_length = f"[cache size: {len(self.history)}]"
        s_running = f"[running: {self.running}]"
        s = f"{self.__class__.__name__} {s_running} {s_idle} {s_cache_length}>"
        return s
