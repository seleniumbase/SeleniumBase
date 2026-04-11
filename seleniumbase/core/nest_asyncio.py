"""Patch asyncio to allow nested event loops."""
import asyncio
import asyncio.events as events
import os
import sys
import threading
from contextlib import contextmanager, suppress
from heapq import heappop

_run_close_loop = True


class PatchedNestAsyncio:
    pass


def apply(loop=None, *, run_close_loop=False, error_on_mispatched=False):
    global _run_close_loop
    _patch_asyncio(error_on_mispatched=error_on_mispatched)
    _patch_policy()
    _patch_tornado()
    loop = loop or _get_event_loop()
    if loop is not None:
        _patch_loop(loop)
    _run_close_loop &= run_close_loop


if sys.version_info < (3, 14, 0):
    def _get_event_loop():
        return asyncio.get_event_loop()
else:
    def _get_event_loop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            return None


if sys.version_info < (3, 12, 0):
    def run(main, *, debug=False):
        loop = asyncio.get_event_loop()
        loop.set_debug(debug)
        task = asyncio.ensure_future(main)
        try:
            return loop.run_until_complete(task)
        finally:
            if not task.done():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    loop.run_until_complete(task)
else:
    def run(main, *, debug=False, loop_factory=None):
        new_event_loop = False
        set_event_loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            if not _run_close_loop:
                loop = _get_event_loop()
                if loop is None:
                    if loop_factory is None:
                        loop_factory = asyncio.new_event_loop
                    loop = loop_factory()
                    asyncio.set_event_loop(loop)
            else:
                if loop_factory is None:
                    loop = asyncio.new_event_loop()
                    set_event_loop = _get_event_loop()
                    asyncio.set_event_loop(loop)
                else:
                    loop = loop_factory()
                new_event_loop = True
        _patch_loop(loop)

        loop.set_debug(debug)
        task = asyncio.ensure_future(main, loop=loop)
        try:
            return loop.run_until_complete(task)
        finally:
            if not task.done():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    loop.run_until_complete(task)
            if set_event_loop:
                asyncio.set_event_loop(set_event_loop)
            if new_event_loop:
                # Avoid ResourceWarning: unclosed event loop
                loop.close()


def _patch_asyncio(*, error_on_mispatched=False):
    """Patch asyncio module to use pure Python tasks and futures."""

    def _get_event_loop(stacklevel=3):
        loop = events._get_running_loop()
        if loop is None:
            if sys.version_info < (3, 14, 0):
                policy = events.get_event_loop_policy()
            else:
                policy = events._get_event_loop_policy()
            loop = policy.get_event_loop()
        return loop

    if hasattr(asyncio, "_nest_patched"):
        if not hasattr(asyncio, "_nest_asyncio"):
            if error_on_mispatched:
                raise RuntimeError("asyncio was already patched!")
            elif sys.version_info >= (3, 12, 0):
                import warnings
                warnings.warn("asyncio was already patched!")
        return

    asyncio.tasks.Task = asyncio.tasks._PyTask
    asyncio.Task = asyncio.tasks._CTask = asyncio.tasks.Task
    asyncio.Future = asyncio.futures._CFuture = asyncio.futures.Future = (
        asyncio.futures._PyFuture
    )
    asyncio.get_event_loop = _get_event_loop
    events._get_event_loop = events.get_event_loop = asyncio.get_event_loop
    asyncio.run = run
    asyncio._nest_patched = True
    asyncio._nest_asyncio = PatchedNestAsyncio()


def _patch_policy():
    """Patch the policy to always return a patched loop."""

    def get_event_loop(self):
        if self._local._loop is None:
            loop = self.new_event_loop()
            _patch_loop(loop)
            self.set_event_loop(loop)
        return self._local._loop

    if sys.version_info < (3, 14, 0):
        policy = events.get_event_loop_policy()
    else:
        policy = events._get_event_loop_policy()
    policy.__class__.get_event_loop = get_event_loop


def _patch_loop(loop):
    """Patch loop to make it reentrant."""

    def run_forever(self):
        with manage_run(self), manage_asyncgens(self):
            while True:
                self._run_once()
                if self._stopping:
                    break
        self._stopping = False

    def run_until_complete(self, future):
        with manage_run(self):
            f = asyncio.ensure_future(future, loop=self)
            if f is not future:
                f._log_destroy_pending = False
            while not f.done():
                self._run_once()
                if self._stopping:
                    break
            if not f.done():
                raise RuntimeError("Loop stopped before Future completed!")
            return f.result()

    def _run_once(self):
        """Simplified re-implementation of asyncio's _run_once."""
        ready = self._ready
        scheduled = self._scheduled
        while scheduled and scheduled[0]._cancelled:
            heappop(scheduled)
        timeout = (
            0
            if ready or self._stopping
            else min(max(scheduled[0]._when - self.time(), 0), 86400)
            if scheduled
            else None
        )
        event_list = self._selector.select(timeout)
        self._process_events(event_list)
        end_time = self.time() + self._clock_resolution
        while scheduled and scheduled[0]._when < end_time:
            handle = heappop(scheduled)
            ready.append(handle)
        for _ in range(len(ready)):
            if not ready:
                break
            handle = ready.popleft()
            if not handle._cancelled:
                if sys.version_info < (3, 14, 0):
                    curr_task = curr_tasks.pop(self, None)
                else:
                    try:
                        curr_task = asyncio.tasks._swap_current_task(
                            self, None
                        )
                    except KeyError:
                        curr_task = None
                try:
                    handle._run()
                finally:
                    if curr_task is not None:
                        if sys.version_info < (3, 14, 0):
                            curr_tasks[self] = curr_task
                        else:
                            asyncio.tasks._swap_current_task(self, curr_task)
        handle = None

    @contextmanager
    def manage_run(self):
        self._check_closed()
        old_thread_id = self._thread_id
        old_running_loop = events._get_running_loop()
        try:
            self._thread_id = threading.get_ident()
            events._set_running_loop(self)
            self._num_runs_pending += 1
            if self._is_proactorloop:
                if self._self_reading_future is None:
                    self.call_soon(self._loop_self_reading)
            yield
        finally:
            self._thread_id = old_thread_id
            events._set_running_loop(old_running_loop)
            self._num_runs_pending -= 1
            if self._is_proactorloop:
                if (
                    self._num_runs_pending == 0
                    and self._self_reading_future is not None
                ):
                    ov = self._self_reading_future._ov
                    self._self_reading_future.cancel()
                    if ov is not None:
                        self._proactor._unregister(ov)
                    self._self_reading_future = None

    @contextmanager
    def manage_asyncgens(self):
        old_agen_hooks = sys.get_asyncgen_hooks()
        try:
            self._set_coroutine_origin_tracking(self._debug)
            if self._asyncgens is not None:
                sys.set_asyncgen_hooks(
                    firstiter=self._asyncgen_firstiter_hook,
                    finalizer=self._asyncgen_finalizer_hook,
                )
            yield
        finally:
            self._set_coroutine_origin_tracking(False)
            if self._asyncgens is not None:
                sys.set_asyncgen_hooks(*old_agen_hooks)

    def _check_running(self):
        """Do not throw exception if loop is already running."""
        pass

    if hasattr(loop, "_nest_patched"):
        return
    if not isinstance(loop, asyncio.BaseEventLoop):
        raise ValueError("Can't patch loop of type %s" % type(loop))
    cls = loop.__class__
    cls.run_forever = run_forever
    cls.run_until_complete = run_until_complete
    cls._run_once = _run_once
    cls._check_running = _check_running
    cls._num_runs_pending = 1 if loop.is_running() else 0
    cls._is_proactorloop = os.name == "nt" and issubclass(
        cls, asyncio.ProactorEventLoop
    )
    curr_tasks = asyncio.tasks._current_tasks
    cls._nest_patched = True
    cls._nest_asyncio = PatchedNestAsyncio()


def _patch_tornado():
    """If tornado is imported before nest_asyncio,
    make tornado aware of the pure-Python asyncio Future."""
    if "tornado" in sys.modules:
        import tornado.concurrent as tc  # type: ignore
        tc.Future = asyncio.Future
        if asyncio.Future not in tc.FUTURES:
            tc.FUTURES += (asyncio.Future,)
