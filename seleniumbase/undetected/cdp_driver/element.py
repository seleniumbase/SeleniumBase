from __future__ import annotations
import asyncio
import json
import logging
import pathlib
import secrets
import typing
from contextlib import suppress
from . import cdp_util as util
from ._contradict import ContraDict
from .config import PathLike
import mycdp as cdp
import mycdp.input_
import mycdp.dom
import mycdp.overlay
import mycdp.page
import mycdp.runtime

logger = logging.getLogger(__name__)
if typing.TYPE_CHECKING:
    from .tab import Tab


def create(
    node: cdp.dom.Node,
    tab: Tab, tree:
    typing.Optional[cdp.dom.Node] = None
):
    """
    Factory for Elements.
    This is used with Tab.query_selector(_all).
    Since we already have the tree,
    we don't need to fetch it for every single element.
    :param node: cdp dom node representation
    :type node: cdp.dom.Node
    :param tab: the target object to which this element belongs
    :type tab: Tab
    :param tree: [Optional] the full node tree to which <node> belongs,
        enhances performance. When not provided, you need to
        call `await elem.update()` before using .children / .parent
    :type tree:
    """
    elem = Element(node, tab, tree)
    return elem


class Element:
    def __init__(
        self, node: cdp.dom.Node, tab: Tab, tree: cdp.dom.Node = None
    ):
        """
        Represents an (HTML) DOM Element
        :param node: cdp dom node representation
        :type node: cdp.dom.Node
        :param tab: the target object to which this element belongs
        :type tab: Tab
        """
        if not node:
            raise Exception("Node cannot be None!")
        self._tab = tab
        # if node.node_name == 'IFRAME':
        #     self._node = node.content_document
        self._node = node
        self._tree = tree
        self._parent = None
        self._remote_object = None
        self._attrs = ContraDict(silent=True)
        self._make_attrs()

    @property
    def tag(self):
        if self.node_name:
            return self.node_name.lower()

    @property
    def tag_name(self):
        return self.tag

    @property
    def node_id(self):
        return self.node.node_id

    @property
    def backend_node_id(self):
        return self.node.backend_node_id

    @property
    def node_type(self):
        return self.node.node_type

    @property
    def node_name(self):
        return self.node.node_name

    @property
    def local_name(self):
        return self.node.local_name

    @property
    def node_value(self):
        return self.node.node_value

    @property
    def parent_id(self):
        return self.node.parent_id

    @property
    def child_node_count(self):
        return self.node.child_node_count

    @property
    def attributes(self):
        return self.node.attributes

    @property
    def document_url(self):
        return self.node.document_url

    @property
    def base_url(self):
        return self.node.base_url

    @property
    def public_id(self):
        return self.node.public_id

    @property
    def system_id(self):
        return self.node.system_id

    @property
    def internal_subset(self):
        return self.node.internal_subset

    @property
    def xml_version(self):
        return self.node.xml_version

    @property
    def value(self):
        return self.node.value

    @property
    def pseudo_type(self):
        return self.node.pseudo_type

    @property
    def pseudo_identifier(self):
        return self.node.pseudo_identifier

    @property
    def shadow_root_type(self):
        return self.node.shadow_root_type

    @property
    def frame_id(self):
        return self.node.frame_id

    @property
    def content_document(self):
        return self.node.content_document

    @property
    def shadow_roots(self):
        return self.node.shadow_roots

    @property
    def template_content(self):
        return self.node.template_content

    @property
    def pseudo_elements(self):
        return self.node.pseudo_elements

    @property
    def imported_document(self):
        return self.node.imported_document

    @property
    def distributed_nodes(self):
        return self.node.distributed_nodes

    @property
    def is_svg(self):
        return self.node.is_svg

    @property
    def compatibility_mode(self):
        return self.node.compatibility_mode

    @property
    def assigned_slot(self):
        return self.node.assigned_slot

    @property
    def tab(self):
        return self._tab

    def __getattr__(self, item):
        # If attribute is not found on the element object,
        # check if it is present in the element attributes
        # (Eg. href=, src=, alt=).
        # Returns None when attribute is not found,
        # instead of raising AttributeError.
        x = getattr(self.attrs, item, None)
        if x:
            return x

    def __setattr__(self, key, value):
        if key[0] != "_":
            if key[1:] not in vars(self).keys():
                self.attrs.__setattr__(key, value)
                return
        super().__setattr__(key, value)

    def __setitem__(self, key, value):
        if key[0] != "_":
            if key[1:] not in vars(self).keys():
                self.attrs[key] = value

    def __getitem__(self, item):
        return self.attrs.get(item, None)

    async def save_to_dom_async(self):
        """Saves element to DOM."""
        self._remote_object = await self._tab.send(
            cdp.dom.resolve_node(backend_node_id=self.backend_node_id)
        )
        await self._tab.send(
            cdp.dom.set_outer_html(self.node_id, outer_html=str(self))
        )
        await self.update()

    async def remove_from_dom_async(self):
        """Removes element from DOM."""
        await self.update()  # Ensure we have latest node_id
        node = util.filter_recurse(
            self._tree,
            lambda node: node.backend_node_id == self.backend_node_id
        )
        if node:
            await self.tab.send(cdp.dom.remove_node(node.node_id))
        # self._tree = util.remove_from_tree(self.tree, self.node)

    async def update(self, _node=None):
        """
        Updates element to retrieve more properties.
        For example this enables:
        :py:obj:`~children` and :py:obj:`~parent` attributes.
        Also resolves js object,
        which is a stored object in :py:obj:`~remote_object`.
        Usually you will get element nodes by the usage of:
        :py:meth:`Tab.query_selector_all()`
        :py:meth:`Tab.find_elements_by_text()`
        Those elements are already updated and you can browse
        through children directly.
        """
        if _node:
            doc = _node
            # self._node = _node
            # self._children.clear()
            self._parent = None
        else:
            doc = await self._tab.send(cdp.dom.get_document(-1, True))
            self._parent = None
        # if self.node_name != "IFRAME":
        updated_node = util.filter_recurse(
            doc, lambda n: n.backend_node_id == self._node.backend_node_id
        )
        if updated_node:
            logger.debug("Node changed, and has now been updated.")
            self._node = updated_node
        self._tree = doc
        self._remote_object = await self._tab.send(
            cdp.dom.resolve_node(backend_node_id=self._node.backend_node_id)
        )
        # self.attrs.clear()
        self._make_attrs()
        if self.node_name != "IFRAME":
            parent_node = util.filter_recurse(
                doc, lambda n: n.node_id == self.node.parent_id
            )
            if not parent_node:
                # Could happen if node is for example <html>
                return self
            self._parent = create(parent_node, tab=self._tab, tree=self._tree)
        return self

    @property
    def node(self):
        return self._node

    @property
    def tree(self) -> cdp.dom.Node:
        return self._tree

    @tree.setter
    def tree(self, tree: cdp.dom.Node):
        self._tree = tree

    @property
    def attrs(self):
        """
        Attributes are stored here.
        You can also set them directly on the element object.
        """
        return self._attrs

    @property
    def parent(self) -> typing.Union[Element, None]:
        """Get the parent element (node) of current element (node)."""
        if not self.tree:
            raise RuntimeError(
                "Could not get parent since the element has no tree set."
            )
        parent_node = util.filter_recurse(
            self.tree, lambda n: n.node_id == self.parent_id
        )
        if not parent_node:
            return None
        parent_element = create(parent_node, tab=self._tab, tree=self.tree)
        return parent_element

    @property
    def children(self) -> typing.Union[typing.List[Element], str]:
        """
        Returns the element's children.
        Those children also have a children property
        so that you can browse through the entire tree as well.
        """
        _children = []
        if self._node.node_name == "IFRAME":
            # iframes are not the same as other nodes.
            # The children of iframes are found under
            # the .content_document property,
            # which is more useful than the node itself.
            frame = self._node.content_document
            if not frame.child_node_count:
                return []
            for child in frame.children:
                child_elem = create(child, self._tab, frame)
                if child_elem:
                    _children.append(child_elem)
            # self._node = frame
            return _children
        elif not self.node.child_node_count:
            return []
        if self.node.children:
            for child in self.node.children:
                child_elem = create(child, self._tab, self.tree)
                if child_elem:
                    _children.append(child_elem)
        return _children

    @property
    def remote_object(self) -> cdp.runtime.RemoteObject:
        return self._remote_object

    @property
    def object_id(self) -> cdp.runtime.RemoteObjectId:
        try:
            return self.remote_object.object_id
        except AttributeError:
            pass

    async def click_async(self):
        """Click the element."""
        self._remote_object = await self._tab.send(
            cdp.dom.resolve_node(
                backend_node_id=self.backend_node_id
            )
        )
        arguments = [cdp.runtime.CallArgument(
            object_id=self._remote_object.object_id
        )]
        await self.flash_async(0.25)
        await self._tab.send(
            cdp.runtime.call_function_on(
                "(el) => el.click()",
                object_id=self._remote_object.object_id,
                arguments=arguments,
                await_promise=True,
                user_gesture=True,
                return_by_value=True,
            )
        )

    async def get_js_attributes_async(self):
        return ContraDict(
            json.loads(
                await self.apply(
                    """
            function (e) {
                let o = {}
                for(let k in e){
                    o[k] = e[k]
                }
                return JSON.stringify(o)
            }
            """
                )
            )
        )

    def __await__(self):
        return self.update().__await__()

    def __call__(self, js_method):
        return self.apply(f"(e) => e['{js_method}']()")

    async def apply(self, js_function, return_by_value=True):
        """
        Apply javascript to this element.
        The given js_function string should accept the js element as parameter,
        and can be a arrow function, or function declaration.
        Eg:
            - '(elem) => {
                    elem.value = "blabla"; consolelog(elem);
                    alert(JSON.stringify(elem);
                } '
            - 'elem => elem.play()'
            - function myFunction(elem) { alert(elem) }
        :param js_function: JS function definition which received this element.
        :param return_by_value:
        """
        self._remote_object = await self._tab.send(
            cdp.dom.resolve_node(backend_node_id=self.backend_node_id)
        )
        result: typing.Tuple[cdp.runtime.RemoteObject, typing.Any] = (
            await self._tab.send(
                cdp.runtime.call_function_on(
                    js_function,
                    object_id=self._remote_object.object_id,
                    arguments=[
                        cdp.runtime.CallArgument(
                            object_id=self._remote_object.object_id
                        )
                    ],
                    return_by_value=True,
                    user_gesture=True,
                )
            )
        )
        if result and result[0]:
            if return_by_value:
                return result[0].value
            return result[0]
        elif result[1]:
            return result[1]

    async def get_position_async(self, abs=False) -> Position:
        if not self.parent or not self.object_id:
            self._remote_object = await self._tab.send(
                cdp.dom.resolve_node(backend_node_id=self.backend_node_id)
            )
            # await self.update()
        try:
            quads = await self.tab.send(
                cdp.dom.get_content_quads(
                    object_id=self.remote_object.object_id
                )
            )
            if not quads:
                raise Exception("Could not find position for %s " % self)
            pos = Position(quads[0])
            if abs:
                scroll_y = (await self.tab.evaluate("window.scrollY")).value
                scroll_x = (await self.tab.evaluate("window.scrollX")).value
                abs_x = pos.left + scroll_x + (pos.width / 2)
                abs_y = pos.top + scroll_y + (pos.height / 2)
                pos.abs_x = abs_x
                pos.abs_y = abs_y
            return pos
        except IndexError:
            logger.debug(
                "No content quads for %s. "
                "Mostly caused by element which is not 'in plain sight'."
                % self
            )

    async def mouse_click_async(
        self,
        button: str = "left",
        buttons: typing.Optional[int] = 1,
        modifiers: typing.Optional[int] = 0,
        hold: bool = False,
        _until_event: typing.Optional[type] = None,
    ):
        """
        Native click (on element).
        Note: This likely does not work at the moment. Use click() instead.
        :param button: str (default = "left")
        :param buttons: which button (default 1 = left)
        :param modifiers: *(Optional)*
                Bit field representing pressed modifier keys.
                Alt=1, Ctrl=2, Meta/Command=4, Shift=8 (default: 0).
        :param _until_event: Internal. Event to wait for before returning.
        """
        try:
            center = (await self.get_position_async()).center
        except AttributeError:
            return
        if not center:
            logger.warning("Could not calculate box model for %s", self)
            return
        logger.debug("Clicking on location: %.2f, %.2f" % center)
        await asyncio.gather(
            self._tab.send(
                cdp.input_.dispatch_mouse_event(
                    "mousePressed",
                    x=center[0],
                    y=center[1],
                    modifiers=modifiers,
                    button=cdp.input_.MouseButton(button),
                    buttons=buttons,
                    click_count=1,
                )
            ),
            self._tab.send(
                cdp.input_.dispatch_mouse_event(
                    "mouseReleased",
                    x=center[0],
                    y=center[1],
                    modifiers=modifiers,
                    button=cdp.input_.MouseButton(button),
                    buttons=buttons,
                    click_count=1,
                )
            ),
        )
        try:
            await self.flash_async()
        except BaseException:
            pass

    async def mouse_move_async(self):
        """
        Moves the mouse to the element position.
        When an element has an hover/mouseover effect, this triggers it.
        """
        try:
            center = (await self.get_position_async()).center
        except AttributeError:
            logger.debug("Did not find location for %s", self)
            return
        logger.debug(
            "Mouse move to location %.2f, %.2f where %s is located",
            *center,
            self,
        )
        await self._tab.send(
            cdp.input_.dispatch_mouse_event(
                "mouseMoved", x=center[0], y=center[1]
            )
        )
        await self._tab.sleep(0.05)
        await self._tab.send(
            cdp.input_.dispatch_mouse_event(
                "mouseReleased", x=center[0], y=center[1]
            )
        )

    async def mouse_drag_async(
        self,
        destination: typing.Union[Element, typing.Tuple[int, int]],
        relative: bool = False,
        steps: int = 1,
    ):
        """
        Drags an element to another element or target coordinates.
        Dragging of elements should be supported by the site.
        :param destination: Another element where to drag to,
            or a tuple (x,y) of ints representing coordinates.
        :type destination: Element or coordinate as x,y tuple
        :param relative: when True, treats coordinate as relative.
        For example (-100, 200) will move left 100px and down 200px.
        :type relative:
        :param steps: Move in <steps> points.
            This could make it look more "natural" (default 1),
            but also a lot slower. (For very smooth actions, use 50-100)
        :type steps: int
        """
        try:
            start_point = (await self.get_position_async()).center
        except AttributeError:
            return
        if not start_point:
            logger.warning("Could not calculate box model for %s", self)
            return
        end_point = None
        if isinstance(destination, Element):
            try:
                end_point = (await destination.get_position_async()).center
            except AttributeError:
                return
            if not end_point:
                logger.warning(
                    "Could not calculate box model for %s", destination
                )
                return
        elif isinstance(destination, (tuple, list)):
            if relative:
                end_point = (
                    start_point[0] + destination[0],
                    start_point[1] + destination[1],
                )
            else:
                end_point = destination
        await self._tab.send(
            cdp.input_.dispatch_mouse_event(
                "mousePressed",
                x=start_point[0],
                y=start_point[1],
                button=cdp.input_.MouseButton("left"),
            )
        )
        steps = 1 if (not steps or steps < 1) else steps
        if steps == 1:
            await self._tab.send(
                cdp.input_.dispatch_mouse_event(
                    "mouseMoved",
                    x=end_point[0],
                    y=end_point[1],
                )
            )
        elif steps > 1:
            step_size_x = (end_point[0] - start_point[0]) / steps
            step_size_y = (end_point[1] - start_point[1]) / steps
            pathway = [
                (
                    start_point[0] + step_size_x * i,
                    start_point[1] + step_size_y * i,
                )
                for i in range(steps + 1)
            ]
            for point in pathway:
                await self._tab.send(
                    cdp.input_.dispatch_mouse_event(
                        "mouseMoved",
                        x=point[0],
                        y=point[1],
                    )
                )
                await asyncio.sleep(0)
        await self._tab.send(
            cdp.input_.dispatch_mouse_event(
                type_="mouseReleased",
                x=end_point[0],
                y=end_point[1],
                button=cdp.input_.MouseButton("left"),
            )
        )

    async def scroll_into_view_async(self):
        """Scrolls element into view."""
        try:
            await self.tab.send(
                cdp.dom.scroll_into_view_if_needed(
                    backend_node_id=self.backend_node_id
                )
            )
        except Exception as e:
            logger.debug("Could not scroll into view: %s", e)
            return
        # await self.apply("""(el) => el.scrollIntoView(false)""")

    async def clear_input_async(self, _until_event: type = None):
        """Clears an input field."""
        try:
            await self.apply('function (element) { element.value = "" } ')
        except Exception as e:
            logger.debug("Could not clear element field: %s", e)
        return

    async def send_keys_async(self, text: str):
        """
        Send text to an input field, or any other html element.
        Hint: If you ever get stuck where using py:meth:`~click`
        does not work, sending the keystroke \\n or \\r\\n
        or a spacebar works wonders!
        :param text: text to send
        :return: None
        """
        await self.apply("(elem) => elem.focus()")
        [
            await self._tab.send(
                cdp.input_.dispatch_key_event("char", text=char)
            )
            for char in list(text)
        ]

    async def send_file_async(self, *file_paths: PathLike):
        """
        Some form input require a file (upload).
        A full path needs to be provided.
        This method sends 1 or more file(s) to the input field.
        Make sure the field accepts multiple files in order to send more files.
        (Otherwise the browser might crash.)
        Example:
        `await fileinputElement.send_file('c:/tmp/img.png', 'c:/dir/lol.gif')`
        """
        file_paths = [str(p) for p in file_paths]
        await self._tab.send(
            cdp.dom.set_file_input_files(
                files=[*file_paths],
                backend_node_id=self.backend_node_id,
                object_id=self.object_id,
            )
        )

    async def focus_async(self):
        """Focus the current element. Often useful in form (select) fields."""
        return await self.apply("(element) => element.focus()")

    async def select_option_async(self):
        """
        For form (select) fields. When you have queried the options
        you can call this method on the option object.
        Calling :func:`option.select_option()` uses option as selected value.
        (Does not work in all cases.)
        """
        if self.node_name == "OPTION":
            await self.apply(
                """
                (o) => {
                    o.selected = true;
                    o.dispatchEvent(new Event(
                        'change', {view: window,bubbles: true})
                    )
                }
                """
            )

    async def set_value_async(self, value):
        await self._tab.send(
            cdp.dom.set_node_value(node_id=self.node_id, value=value)
        )

    async def set_text_async(self, value):
        if not self.node_type == 3:
            if self.child_node_count == 1:
                child_node = self.children[0]
                await child_node.set_text_async(value)
                await self.update()
                return
            else:
                raise RuntimeError("Could only set value of text nodes.")
        await self.update()
        await self._tab.send(
            cdp.dom.set_node_value(node_id=self.node_id, value=value)
        )

    async def get_html_async(self):
        return await self._tab.send(
            cdp.dom.get_outer_html(backend_node_id=self.backend_node_id)
        )

    @property
    def text_fragment(self) -> str:
        """Gets the text content of this specific element node."""
        text_node = util.filter_recurse(self.node, lambda n: n.node_type == 3)
        if text_node:
            return text_node.node_value.strip()
        return ""

    @property
    def text(self):
        """
        Gets the text contents of this element and child nodes, concatenated.
        Note: This includes text in the form of script content, (text nodes).
        """
        with suppress(Exception):
            if self.node.node_name.lower() in ["input", "textarea"]:
                input_node = self.node.shadow_roots[0].children[0].children[0]
                if input_node:
                    return input_node.node_value
        text_nodes = util.filter_recurse_all(
            self.node, lambda n: n.node_type == 3
        )
        return " ".join([n.node_value for n in text_nodes]).strip()

    @property
    def text_all(self):
        """Same as text(). Kept for backwards compatibility."""
        with suppress(Exception):
            if self.node.node_name.lower() in ["input", "textarea"]:
                input_node = self.node.shadow_roots[0].children[0].children[0]
                if input_node:
                    return input_node.node_value
        text_nodes = util.filter_recurse_all(
            self.node, lambda n: n.node_type == 3
        )
        return " ".join([n.node_value for n in text_nodes]).strip()

    async def query_selector_all_async(self, selector: str):
        """Like JS querySelectorAll()"""
        await self.update()
        return await self.tab.query_selector_all(selector, _node=self)

    async def query_selector_async(self, selector: str):
        """Like JS querySelector()"""
        await self.update()
        return await self.tab.query_selector(selector, self)

    async def save_screenshot_async(
        self,
        filename: typing.Optional[PathLike] = "auto",
        format: typing.Optional[str] = "png",
        scale: typing.Optional[typing.Union[int, float]] = 1,
    ):
        """
        Saves a screenshot of this element (only).
        This is not the same as :py:obj:`Tab.save_screenshot`,
        which saves a "regular" screenshot.
        When the element is hidden, or has no size,
        or is otherwise not capturable, a RuntimeError is raised.
        :param filename: uses this as the save path
        :type filename: PathLike
        :param format: jpeg or png (defaults to png)
        :type format: str
        :param scale: the scale of the screenshot,
         eg: 1 = size as is, 2 = double, 0.5 is half.
        :return: the path/filename of saved screenshot
        :rtype: str
        """
        import urllib.parse
        import datetime
        import base64

        pos = await self.get_position_async()
        if not pos:
            raise RuntimeError(
                "Could not determine position of element. "
                "Probably because it's not in view, or hidden."
            )
        viewport = pos.to_viewport(scale)
        path = None
        await self.tab.sleep()
        if not filename or filename == "auto":
            parsed = urllib.parse.urlparse(self.tab.target.url)
            parts = parsed.path.split("/")
            last_part = parts[-1]
            last_part = last_part.rsplit("?", 1)[0]
            dt_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            candidate = f"{parsed.hostname}__{last_part}_{dt_str}"
            ext = ""
            if format.lower() in ["jpg", "jpeg"]:
                ext = ".jpg"
                format = "jpeg"
            elif format.lower() in ["png"]:
                ext = ".png"
                format = "png"
            path = pathlib.Path(candidate + ext)
        else:
            if filename.lower().endswith(".png"):
                format = "png"
            elif (
                filename.lower().endswith(".jpg")
                or filename.lower().endswith(".jpeg")
            ):
                format = "jpeg"
            path = pathlib.Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = await self._tab.send(
            cdp.page.capture_screenshot(
                format, clip=viewport, capture_beyond_viewport=True
            )
        )
        if not data:
            from .connection import ProtocolException

            raise ProtocolException(
                "Could not take screenshot. "
                "Most possible cause is the page has not finished loading yet."
            )
        data_bytes = base64.b64decode(data)
        if not path:
            raise RuntimeError("Invalid filename or path: '%s'" % filename)
        path.write_bytes(data_bytes)
        return str(path)

    async def flash_async(
        self,
        duration: typing.Union[float, int] = 0.5,
        color: typing.Optional[str] = "EE4488",
    ):
        """
        Displays for a short time a red dot on the element.
        (Only if the element itself is visible)
        :param coords: x,y
        :param duration: seconds (default 0.5)
        """
        from .connection import ProtocolException

        if not self.remote_object:
            try:
                self._remote_object = await self.tab.send(
                    cdp.dom.resolve_node(backend_node_id=self.backend_node_id)
                )
            except ProtocolException:
                return
        try:
            pos = await self.get_position_async()
        except (Exception,):
            logger.debug("flash() : Could not determine position.")
            return
        style = (
            "position:absolute;z-index:99999999;padding:0;margin:0;"
            "left:{:.1f}px; top: {:.1f}px; opacity:0.7;"
            "width:8px;height:8px;border-radius:50%;background:#{};"
            "animation:show-pointer-ani {:.2f}s ease 1;"
        ).format(
            pos.center[0] - 4,  # -4 to account for drawn circle itself (w,h)
            pos.center[1] - 4,
            color,
            duration,
        )
        script = (
            """
            (targetElement) => {{
                var css = document.styleSheets[0];
                for( let css of [...document.styleSheets]) {{
                    try {{
                        css.insertRule(`
                        @keyframes show-pointer-ani {{
                              0% {{ opacity: 1; transform: scale(2, 2);}}
                              25% {{ transform: scale(5,5) }}
                              50% {{ transform: scale(3, 3);}}
                              75%: {{ transform: scale(2,2) }}
                              100% {{ transform: scale(1, 1); opacity: 0;}}
                        }}`,css.cssRules.length);
                        break;
                    }} catch (e) {{
                        console.log(e)
                    }}
                }};
                var _d = document.createElement('div');
                _d.style = `{0:s}`;
                _d.id = `{1:s}`;
                document.body.insertAdjacentElement('afterBegin', _d);
                setTimeout(
                    () => document.getElementById('{1:s}').remove(), {2:d}
                );
            }}
            """.format(
                style,
                secrets.token_hex(8),
                int(duration * 1000),
            )
            .replace("  ", "")
            .replace("\n", "")
        )
        arguments = [cdp.runtime.CallArgument(
            object_id=self._remote_object.object_id
        )]
        await self._tab.send(
            cdp.runtime.call_function_on(
                script,
                object_id=self._remote_object.object_id,
                arguments=arguments,
                await_promise=True,
                user_gesture=True,
            )
        )

    async def highlight_overlay_async(self):
        """
        Highlights the element devtools-style.
        To remove the highlight, call the method again.
        """
        if getattr(self, "_is_highlighted", False):
            del self._is_highlighted
            await self.tab.send(cdp.overlay.hide_highlight())
            await self.tab.send(cdp.dom.disable())
            await self.tab.send(cdp.overlay.disable())
            return
        await self.tab.send(cdp.dom.enable())
        await self.tab.send(cdp.overlay.enable())
        conf = cdp.overlay.HighlightConfig(
            show_info=True, show_extension_lines=True, show_styles=True
        )
        await self.tab.send(
            cdp.overlay.highlight_node(
                highlight_config=conf, backend_node_id=self.backend_node_id
            )
        )
        setattr(self, "_is_highlighted", 1)

    async def record_video_async(
        self,
        filename: typing.Optional[str] = None,
        folder: typing.Optional[str] = None,
        duration: typing.Optional[typing.Union[int, float]] = None,
    ):
        """
        Experimental option.
        :param filename: the desired filename
        :param folder: the download folder path
        :param duration: record for this many seconds and then download
        On html5 video nodes,
        you can call this method to start recording of the video.
        When any of the follow happens, the video recorded will be downloaded:
            - video ends
            - calling videoelement('pause')
            - video stops
        """
        if self.node_name != "VIDEO":
            raise RuntimeError(
                "record_video() can only be called on html5 video elements"
            )
        if not folder:
            directory_path = pathlib.Path.cwd() / "downloads"
        else:
            directory_path = pathlib.Path(folder)
        directory_path.mkdir(exist_ok=True)
        await self._tab.send(
            cdp.browser.set_download_behavior(
                "allow", download_path=str(directory_path)
            )
        )
        await self("pause")
        dtm = 'document.title + ".mp4"'
        await self.apply(
            """
            function extractVid(vid) {{
                    var duration = {duration:.1f};
                    var stream = vid.captureStream();
                    var mr = new MediaRecorder(
                        stream, {{audio:true, video:true}}
                    )
                    mr.ondataavailable  = function(e) {{
                        vid['_recording'] = false
                        var blob = e.data;
                        f = new File(
                            [blob], {{name: {filename}, type:'octet/stream'}}
                        );
                        var objectUrl = URL.createObjectURL(f);
                        var link = document.createElement('a');
                        link.setAttribute('href', objectUrl)
                        link.setAttribute('download', {filename})
                        link.style.display = 'none'
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                    }}
                    mr.start()
                    vid.addEventListener('ended' , (e) => mr.stop())
                    vid.addEventListener('pause' , (e) => mr.stop())
                    vid.addEventListener('abort', (e) => mr.stop())
                    if ( duration ) {{
                        setTimeout(
                            () => {{ vid.pause(); vid.play() }}, duration
                        );
                    }}
                    vid['_recording'] = true
            ;}}
            """.format(
                filename=f'"{filename}"' if filename else dtm,
                duration=int(duration * 1000) if duration else 0,
            )
        )
        await self("play")
        await self._tab

    async def is_recording_async(self):
        return await self.apply('(vid) => vid["_recording"]')

    def _make_attrs(self):
        sav = None
        if self.node.attributes:
            for i, a in enumerate(self.node.attributes):
                if i == 0 or i % 2 == 0:
                    if a == "class":
                        a = "class_"
                    sav = a
                else:
                    if sav:
                        self.attrs[sav] = a

    def __eq__(self, other: Element) -> bool:
        # if other.__dict__.values() == self.__dict__.values():
        #     return True
        if other.backend_node_id and self.backend_node_id:
            return other.backend_node_id == self.backend_node_id
        return False

    def __repr__(self):
        tag_name = self.node.node_name.lower()
        content = ""
        # Collect all text from this leaf.
        if self.child_node_count:
            if self.child_node_count == 1:
                if self.children:
                    content += str(self.children[0])
            elif self.child_node_count > 1:
                if self.children:
                    for child in self.children:
                        content += str(child)
        if self.node.node_type == 3:  # Could be a text node
            content += self.node_value
            # Return text only. (No tag names)
            # This makes it look most natural.
            return content
        attrs = " ".join(
            [
                f'{k if k != "class_" else "class"}="{v}"'
                for k, v in self.attrs.items()
            ]
        )
        s = f"<{tag_name} {attrs}>{content}</{tag_name}>"
        return s


class Position(cdp.dom.Quad):
    """Helper class for element-positioning."""

    def __init__(self, points):
        super().__init__(points)
        (
            self.left,
            self.top,
            self.right,
            self.top,
            self.right,
            self.bottom,
            self.left,
            self.bottom,
        ) = points
        self.abs_x: float = 0
        self.abs_y: float = 0
        self.x = self.left
        self.y = self.top
        self.height, self.width = (
            self.bottom - self.top, self.right - self.left
        )
        self.center = (
            self.left + (self.width / 2),
            self.top + (self.height / 2),
        )

    def to_viewport(self, scale=1):
        return cdp.page.Viewport(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            scale=scale,
        )

    def __repr__(self):
        return (
            f"""<Position(x={self.left}, y={self.top},
            width={self.width}, height={self.height})>
            """
        )


async def resolve_node(tab: Tab, node_id: cdp.dom.NodeId):
    remote_obj: cdp.runtime.RemoteObject = await tab.send(
        cdp.dom.resolve_node(node_id=node_id)
    )
    node_id: cdp.dom.NodeId = await tab.send(cdp.dom.request_node(
        remote_obj.object_id
    ))
    node: cdp.dom.Node = await tab.send(cdp.dom.describe_node(node_id))
    return node
