from functools import partial
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from prompt_toolkit.application.current import get_app
from prompt_toolkit.cache import SimpleCache
from prompt_toolkit.data_structures import Point
from prompt_toolkit.filters import (
    FilterOrBool,
    to_filter,
)
from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    StyleAndTextTuples,
    to_formatted_text,
)
from prompt_toolkit.formatted_text.utils import (
    fragment_list_to_text,
    fragment_list_width,
)
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container, UIControl, AnyDimension, Margin, ScrollOffsets, ColorColumn, WindowAlign, \
    WindowRenderInfo, to_dimension, Dimension
import prompt_toolkit.layout.containers
from prompt_toolkit.layout.controls import GetLinePrefixCallable, DummyControl, UIContent, FormattedTextControl
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.layout.screen import Screen, WritePosition, _CHAR_CACHE
from prompt_toolkit.layout.utils import explode_text_fragments
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.utils import get_cwidth, to_str


class TestWindow(Window):
    """
    Container that holds a control.

    :param content: :class:`.UIControl` instance.
    :param width: :class:`.Dimension` instance or callable.
    :param height: :class:`.Dimension` instance or callable.
    :param z_index: When specified, this can be used to bring element in front
        of floating elements.
    :param dont_extend_width: When `True`, don't take up more width then the
                              preferred width reported by the control.
    :param dont_extend_height: When `True`, don't take up more width then the
                               preferred height reported by the control.
    :param ignore_content_width: A `bool` or :class:`.Filter` instance. Ignore
        the :class:`.UIContent` width when calculating the dimensions.
    :param ignore_content_height: A `bool` or :class:`.Filter` instance. Ignore
        the :class:`.UIContent` height when calculating the dimensions.
    :param left_margins: A list of :class:`.Margin` instance to be displayed on
        the left. For instance: :class:`~prompt_toolkit.layout.NumberedMargin`
        can be one of them in order to show line numbers.
    :param right_margins: Like `left_margins`, but on the other side.
    :param scroll_offsets: :class:`.ScrollOffsets` instance, representing the
        preferred amount of lines/columns to be always visible before/after the
        cursor. When both top and bottom are a very high number, the cursor
        will be centered vertically most of the time.
    :param allow_scroll_beyond_bottom: A `bool` or
        :class:`.Filter` instance. When True, allow scrolling so far, that the
        top part of the content is not visible anymore, while there is still
        empty space available at the bottom of the window. In the Vi editor for
        instance, this is possible. You will see tildes while the top part of
        the body is hidden.
    :param wrap_lines: A `bool` or :class:`.Filter` instance. When True, don't
        scroll horizontally, but wrap lines instead.
    :param get_vertical_scroll: Callable that takes this window
        instance as input and returns a preferred vertical scroll.
        (When this is `None`, the scroll is only determined by the last and
        current cursor position.)
    :param get_horizontal_scroll: Callable that takes this window
        instance as input and returns a preferred vertical scroll.
    :param always_hide_cursor: A `bool` or
        :class:`.Filter` instance. When True, never display the cursor, even
        when the user control specifies a cursor position.
    :param cursorline: A `bool` or :class:`.Filter` instance. When True,
        display a cursorline.
    :param cursorcolumn: A `bool` or :class:`.Filter` instance. When True,
        display a cursorcolumn.
    :param colorcolumns: A list of :class:`.ColorColumn` instances that
        describe the columns to be highlighted, or a callable that returns such
        a list.
    :param align: :class:`.WindowAlign` value or callable that returns an
        :class:`.WindowAlign` value. alignment of content.
    :param style: A style string. Style to be applied to all the cells in this
        window. (This can be a callable that returns a string.)
    :param char: (string) Character to be used for filling the background. This
        can also be a callable that returns a character.
    :param get_line_prefix: None or a callable that returns formatted text to
        be inserted before a line. It takes a line number (int) and a
        wrap_count and returns formatted text. This can be used for
        implementation of line continuations, things like Vim "breakindent" and
        so on.
    """

    def __init__(
            self,
            content: Optional[UIControl] = None,
            width: AnyDimension = None,
            height: AnyDimension = None,
            z_index: Optional[int] = None,
            dont_extend_width: FilterOrBool = False,
            dont_extend_height: FilterOrBool = False,
            ignore_content_width: FilterOrBool = False,
            ignore_content_height: FilterOrBool = False,
            left_margins: Optional[Sequence[Margin]] = None,
            right_margins: Optional[Sequence[Margin]] = None,
            scroll_offsets: Optional[ScrollOffsets] = None,
            allow_scroll_beyond_bottom: FilterOrBool = False,
            wrap_lines: FilterOrBool = False,
            get_vertical_scroll: Optional[Callable[["TestWindow"], int]] = None,
            get_horizontal_scroll: Optional[Callable[["TestWindow"], int]] = None,
            always_hide_cursor: FilterOrBool = False,
            cursorline: FilterOrBool = False,
            cursorcolumn: FilterOrBool = False,
            colorcolumns: Union[
                None, List[ColorColumn], Callable[[], List[ColorColumn]]
            ] = None,
            align: Union[WindowAlign, Callable[[], WindowAlign]] = WindowAlign.LEFT,
            style: Union[str, Callable[[], str]] = "",
            char: Union[None, str, Callable[[], str]] = None,
            get_line_prefix: Optional[GetLinePrefixCallable] = None,
    ) -> None:

        self.allow_scroll_beyond_bottom = to_filter(allow_scroll_beyond_bottom)
        self.always_hide_cursor = to_filter(always_hide_cursor)
        self.wrap_lines = to_filter(wrap_lines)
        self.cursorline = to_filter(cursorline)
        self.cursorcolumn = to_filter(cursorcolumn)

        self.content = content or DummyControl()
        self.dont_extend_width = to_filter(dont_extend_width)
        self.dont_extend_height = to_filter(dont_extend_height)
        self.ignore_content_width = to_filter(ignore_content_width)
        self.ignore_content_height = to_filter(ignore_content_height)
        self.left_margins = left_margins or []
        self.right_margins = right_margins or []
        self.scroll_offsets = scroll_offsets or ScrollOffsets()
        self.get_vertical_scroll = get_vertical_scroll
        self.get_horizontal_scroll = get_horizontal_scroll
        self.colorcolumns = colorcolumns or []
        self.align = align
        self.style = style
        self.char = char
        self.get_line_prefix = get_line_prefix

        self.width = width
        self.height = height
        self.z_index = z_index

        # Cache for the screens generated by the margin.
        self._ui_content_cache: SimpleCache[
            Tuple[int, int, int], UIContent
        ] = SimpleCache(maxsize=8)
        self._margin_width_cache: SimpleCache[Tuple[Margin, int], int] = SimpleCache(
            maxsize=1
        )

        self.reset()

    def __repr__(self) -> str:
        return "Window(content=%r)" % self.content

    def reset(self) -> None:
        self.content.reset()

        #: Scrolling position of the main content.
        self.vertical_scroll = 0
        self.horizontal_scroll = 0

        # Vertical scroll 2: this is the vertical offset that a line is
        # scrolled if a single line (the one that contains the cursor) consumes
        # all of the vertical space.
        self.vertical_scroll_2 = 0

        #: Keep render information (mappings between buffer input and render
        #: output.)
        self.render_info: Optional[WindowRenderInfo] = None

    def _get_margin_width(self, margin: Margin) -> int:
        """
        Return the width for this margin.
        (Calculate only once per render time.)
        """

        # Margin.get_width, needs to have a UIContent instance.
        def get_ui_content() -> UIContent:
            return self._get_ui_content(width=0, height=0)

        def get_width() -> int:
            return margin.get_width(get_ui_content)

        key = (margin, get_app().render_counter)
        return self._margin_width_cache.get(key, get_width)

    def _get_total_margin_width(self) -> int:
        """
        Calculate and return the width of the margin (left + right).
        """
        return sum(self._get_margin_width(m) for m in self.left_margins) + sum(
            self._get_margin_width(m) for m in self.right_margins
        )

    def preferred_width(self, max_available_width: int) -> Dimension:
        """
        Calculate the preferred width for this window.
        """

        def preferred_content_width() -> Optional[int]:
            """Content width: is only calculated if no exact width for the
            window was given."""
            if self.ignore_content_width():
                return None

            # Calculate the width of the margin.
            total_margin_width = self._get_total_margin_width()

            # Window of the content. (Can be `None`.)
            preferred_width = self.content.preferred_width(
                max_available_width - total_margin_width
            )

            if preferred_width is not None:
                # Include width of the margins.
                preferred_width += total_margin_width
            return preferred_width

        # Merge.
        return self._merge_dimensions(
            dimension=to_dimension(self.width),
            get_preferred=preferred_content_width,
            dont_extend=self.dont_extend_width(),
        )

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        """
        Calculate the preferred height for this window.
        """

        def preferred_content_height() -> Optional[int]:
            """Content height: is only calculated if no exact height for the
            window was given."""
            if self.ignore_content_height():
                return None

            total_margin_width = self._get_total_margin_width()
            wrap_lines = self.wrap_lines()

            return self.content.preferred_height(
                width - total_margin_width,
                max_available_height,
                wrap_lines,
                self.get_line_prefix,
            )

        return self._merge_dimensions(
            dimension=to_dimension(self.height),
            get_preferred=preferred_content_height,
            dont_extend=self.dont_extend_height(),
        )

    @staticmethod
    def _merge_dimensions(
            dimension: Optional[Dimension],
            get_preferred: Callable[[], Optional[int]],
            dont_extend: bool = False,
    ) -> Dimension:
        """
        Take the Dimension from this `Window` class and the received preferred
        size from the `UIControl` and return a `Dimension` to report to the
        parent container.
        """
        dimension = dimension or Dimension()

        # When a preferred dimension was explicitly given to the Window,
        # ignore the UIControl.
        preferred: Optional[int]

        if dimension.preferred_specified:
            preferred = dimension.preferred
        else:
            # Otherwise, calculate the preferred dimension from the UI control
            # content.
            preferred = get_preferred()

        # When a 'preferred' dimension is given by the UIControl, make sure
        # that it stays within the bounds of the Window.
        if preferred is not None:
            if dimension.max_specified:
                preferred = min(preferred, dimension.max)

            if dimension.min_specified:
                preferred = max(preferred, dimension.min)

        # When a `dont_extend` flag has been given, use the preferred dimension
        # also as the max dimension.
        max_: Optional[int]
        min_: Optional[int]

        if dont_extend and preferred is not None:
            max_ = min(dimension.max, preferred)
        else:
            max_ = dimension.max if dimension.max_specified else None

        min_ = dimension.min if dimension.min_specified else None

        return Dimension(
            min=min_, max=max_, preferred=preferred, weight=dimension.weight
        )

    def _get_ui_content(self, width: int, height: int) -> UIContent:
        """
        Create a `UIContent` instance.
        """

        def get_content() -> UIContent:
            return self.content.create_content(width=width, height=height)

        key = (get_app().render_counter, width, height)
        return self._ui_content_cache.get(key, get_content)

    def _get_digraph_char(self) -> Optional[str]:
        " Return `False`, or the Digraph symbol to be used. "
        app = get_app()
        if app.quoted_insert:
            return "^"
        if app.vi_state.waiting_for_digraph:
            if app.vi_state.digraph_symbol1:
                return app.vi_state.digraph_symbol1
            return "?"
        return None

    def write_to_screen(
            self,
            screen: Screen,
            mouse_handlers: MouseHandlers,
            write_position: WritePosition,
            parent_style: str,
            erase_bg: bool,
            z_index: Optional[int],
    ) -> None:
        """
        Write window to screen. This renders the user control, the margins and
        copies everything over to the absolute position at the given screen.
        """
        z_index = z_index if self.z_index is None else self.z_index

        draw_func = partial(
            self._write_to_screen_at_index,
            screen,
            mouse_handlers,
            write_position,
            parent_style,
            erase_bg,
        )

        if z_index is None or z_index <= 0:
            # When no z_index is given, draw right away.
            draw_func()
        else:
            # Otherwise, postpone.
            screen.draw_with_z_index(z_index=z_index, draw_func=draw_func)

    def _write_to_screen_at_index(
            self,
            screen: Screen,
            mouse_handlers: MouseHandlers,
            write_position: WritePosition,
            parent_style: str,
            erase_bg: bool,
    ) -> None:
        # Don't bother writing invisible windows.
        # (We save some time, but also avoid applying last-line styling.)
        if write_position.height <= 0 or write_position.width <= 0:
            return

        # Calculate margin sizes.
        left_margin_widths = [self._get_margin_width(m) for m in self.left_margins]
        right_margin_widths = [self._get_margin_width(m) for m in self.right_margins]
        total_margin_width = sum(left_margin_widths + right_margin_widths)

        # Render UserControl.
        ui_content = self.content.create_content(
            write_position.width - total_margin_width, write_position.height
        )
        assert isinstance(ui_content, UIContent)

        # Scroll content.
        wrap_lines = self.wrap_lines()
        self._scroll(
            ui_content, write_position.width - total_margin_width, write_position.height
        )

        # Erase background and fill with `char`.
        self._fill_bg(screen, write_position, erase_bg)

        # Resolve `align` attribute.
        align = self.align() if callable(self.align) else self.align

        # Write body
        visible_line_to_row_col, rowcol_to_yx = self._copy_body(
            ui_content,
            screen,
            write_position,
            sum(left_margin_widths),
            write_position.width - total_margin_width,
            self.vertical_scroll,
            self.horizontal_scroll,
            wrap_lines=wrap_lines,
            highlight_lines=True,
            vertical_scroll_2=self.vertical_scroll_2,
            always_hide_cursor=self.always_hide_cursor(),
            has_focus=get_app().layout.current_control == self.content,
            align=align,
            get_line_prefix=self.get_line_prefix,
        )

        # Remember render info. (Set before generating the margins. They need this.)
        x_offset = write_position.xpos + sum(left_margin_widths)
        y_offset = write_position.ypos

        render_info = WindowRenderInfo(
            window=self,
            ui_content=ui_content,
            horizontal_scroll=self.horizontal_scroll,
            vertical_scroll=self.vertical_scroll,
            window_width=write_position.width - total_margin_width,
            window_height=write_position.height,
            configured_scroll_offsets=self.scroll_offsets,
            visible_line_to_row_col=visible_line_to_row_col,
            rowcol_to_yx=rowcol_to_yx,
            x_offset=x_offset,
            y_offset=y_offset,
            wrap_lines=wrap_lines,
        )
        self.render_info = render_info

        # Set mouse handlers.
        def mouse_handler(mouse_event: MouseEvent) -> None:
            """Wrapper around the mouse_handler of the `UIControl` that turns
            screen coordinates into line coordinates."""
            # Don't handle mouse events outside of the current modal part of
            # the UI.
            if self not in get_app().layout.walk_through_modal_area():
                return

            # Find row/col position first.
            yx_to_rowcol = {v: k for k, v in rowcol_to_yx.items()}
            y = mouse_event.position.y
            x = mouse_event.position.x

            # If clicked below the content area, look for a position in the
            # last line instead.
            max_y = write_position.ypos + len(visible_line_to_row_col) - 1
            y = min(max_y, y)
            result: prompt_toolkit.layout.containers.NotImplementedOrNone

            while x >= 0:
                try:
                    row, col = yx_to_rowcol[y, x]
                except KeyError:
                    # Try again. (When clicking on the right side of double
                    # width characters, or on the right side of the input.)
                    x -= 1
                else:
                    # Found position, call handler of UIControl.
                    result = self.content.mouse_handler(
                        MouseEvent(
                            position=Point(x=col, y=row),
                            event_type=mouse_event.event_type,
                        )
                    )
                    break
            else:
                # nobreak.
                # (No x/y coordinate found for the content. This happens in
                # case of a DummyControl, that does not have any content.
                # Report (0,0) instead.)
                result = self.content.mouse_handler(
                    MouseEvent(
                        position=Point(x=0, y=0), event_type=mouse_event.event_type
                    )
                )

            # If it returns NotImplemented, handle it here.
            if result == NotImplemented:
                self._mouse_handler(mouse_event)

        mouse_handlers.set_mouse_handler_for_range(
            x_min=write_position.xpos + sum(left_margin_widths),
            x_max=write_position.xpos + write_position.width - total_margin_width,
            y_min=write_position.ypos,
            y_max=write_position.ypos + write_position.height,
            handler=mouse_handler,
        )

        # Render and copy margins.
        move_x = 0

        def render_margin(m: Margin, width: int) -> UIContent:
            " Render margin. Return `Screen`. "
            # Retrieve margin fragments.
            fragments = m.create_margin(render_info, width, write_position.height)

            # Turn it into a UIContent object.
            # already rendered those fragments using this size.)
            return FormattedTextControl(fragments).create_content(
                width + 1, write_position.height
            )

        for m, width in zip(self.left_margins, left_margin_widths):
            if width > 0:  # (ConditionalMargin returns a zero width. -- Don't render.)
                # Create screen for margin.
                margin_content = render_margin(m, width)

                # Copy and shift X.
                self._copy_margin(margin_content, screen, write_position, move_x, width)
                move_x += width

        move_x = write_position.width - sum(right_margin_widths)

        for m, width in zip(self.right_margins, right_margin_widths):
            # Create screen for margin.
            margin_content = render_margin(m, width)

            # Copy and shift X.
            self._copy_margin(margin_content, screen, write_position, move_x, width)
            move_x += width

        # Apply 'self.style'
        self._apply_style(screen, write_position, parent_style)

        # Tell the screen that this user control has been painted.
        screen.visible_windows.append(self)

    def _copy_body(
            self,
            ui_content: UIContent,
            new_screen: Screen,
            write_position: WritePosition,
            move_x: int,
            width: int,
            vertical_scroll: int = 0,
            horizontal_scroll: int = 0,
            wrap_lines: bool = False,
            highlight_lines: bool = False,
            vertical_scroll_2: int = 0,
            always_hide_cursor: bool = False,
            has_focus: bool = False,
            align: WindowAlign = WindowAlign.LEFT,
            get_line_prefix: Optional[Callable[[int, int], AnyFormattedText]] = None,
    ) -> Tuple[Dict[int, Tuple[int, int]], Dict[Tuple[int, int], Tuple[int, int]]]:
        """
        Copy the UIContent into the output screen.
        Return (visible_line_to_row_col, rowcol_to_yx) tuple.

        :param get_line_prefix: None or a callable that takes a line number
            (int) and a wrap_count (int) and returns formatted text.
        """
        xpos = write_position.xpos + move_x
        ypos = write_position.ypos
        line_count = ui_content.line_count
        new_buffer = new_screen.data_buffer
        empty_char = _CHAR_CACHE["", ""]

        # Map visible line number to (row, col) of input.
        # 'col' will always be zero if line wrapping is off.
        visible_line_to_row_col: Dict[int, Tuple[int, int]] = {}

        # Maps (row, col) from the input to (y, x) screen coordinates.
        rowcol_to_yx: Dict[Tuple[int, int], Tuple[int, int]] = {}

        def copy_line(
                line: StyleAndTextTuples,
                lineno: int,
                x: int,
                y: int,
                is_input: bool = False,
        ) -> Tuple[int, int]:
            """
            Copy over a single line to the output screen. This can wrap over
            multiple lines in the output. It will call the prefix (prompt)
            function before every line.
            """
            if is_input:
                current_rowcol_to_yx = rowcol_to_yx
            else:
                current_rowcol_to_yx = {}  # Throwaway dictionary.

            # Draw line prefix.
            if is_input and get_line_prefix:
                prompt = to_formatted_text(get_line_prefix(lineno, 0))
                x, y = copy_line(prompt, lineno, x, y, is_input=False)

            # Scroll horizontally.
            skipped = 0  # Characters skipped because of horizontal scrolling.
            if horizontal_scroll and is_input:
                h_scroll = horizontal_scroll
                line = explode_text_fragments(line)
                while h_scroll > 0 and line:
                    h_scroll -= get_cwidth(line[0][1])
                    skipped += 1
                    del line[:1]  # Remove first character.

                x -= h_scroll  # When scrolling over double width character,
                # this can end up being negative.

            # Align this line. (Note that this doesn't work well when we use
            # get_line_prefix and that function returns variable width prefixes.)
            if align == WindowAlign.CENTER:
                line_width = fragment_list_width(line)
                if line_width < width:
                    x += (width - line_width) // 2
            elif align == WindowAlign.RIGHT:
                line_width = fragment_list_width(line)
                if line_width < width:
                    x += width - line_width

            col = 0
            wrap_count = 0
            for style, text, *_ in line:
                new_buffer_row = new_buffer[y + ypos]

                # Remember raw VT escape sequences. (E.g. FinalTerm's
                # escape sequences.)
                if "[ZeroWidthEscape]" in style:
                    new_screen.zero_width_escapes[y + ypos][x + xpos] += text
                    continue

                for c in text:
                    char = _CHAR_CACHE[c, style]
                    char_width = char.width

                    # Wrap when the line width is exceeded.
                    if wrap_lines and x + char_width > width:
                        visible_line_to_row_col[y + 1] = (
                            lineno,
                            visible_line_to_row_col[y][1] + x,
                        )
                        y += 1
                        wrap_count += 1
                        x = 0

                        # Insert line prefix (continuation prompt).
                        if is_input and get_line_prefix:
                            prompt = to_formatted_text(
                                get_line_prefix(lineno, wrap_count)
                            )
                            x, y = copy_line(prompt, lineno, x, y, is_input=False)

                        new_buffer_row = new_buffer[y + ypos]

                        if y >= write_position.height:
                            return x, y  # Break out of all for loops.

                    # Set character in screen and shift 'x'.
                    if x >= 0 and y >= 0 and x < write_position.width:
                        new_buffer_row[x + xpos] = char

                        # When we print a multi width character, make sure
                        # to erase the neighbours positions in the screen.
                        # (The empty string if different from everything,
                        # so next redraw this cell will repaint anyway.)
                        if char_width > 1:
                            for i in range(1, char_width):
                                new_buffer_row[x + xpos + i] = empty_char

                        # If this is a zero width characters, then it's
                        # probably part of a decomposed unicode character.
                        # See: https://en.wikipedia.org/wiki/Unicode_equivalence
                        # Merge it in the previous cell.
                        elif char_width == 0:
                            # Handle all character widths. If the previous
                            # character is a multiwidth character, then
                            # merge it two positions back.
                            for pw in [2, 1]:  # Previous character width.
                                if (
                                        x - pw >= 0
                                        and new_buffer_row[x + xpos - pw].width == pw
                                ):
                                    prev_char = new_buffer_row[x + xpos - pw]
                                    char2 = _CHAR_CACHE[
                                        prev_char.char + c, prev_char.style
                                    ]
                                    new_buffer_row[x + xpos - pw] = char2

                        # Keep track of write position for each character.
                        current_rowcol_to_yx[lineno, col + skipped] = (
                            y + ypos,
                            x + xpos,
                        )

                    col += 1
                    x += char_width
            return x, y

        # Copy content.
        def copy() -> int:
            y = -vertical_scroll_2
            lineno = vertical_scroll

            while y < write_position.height and lineno < line_count:
                # Take the next line and copy it in the real screen.
                line = ui_content.get_line(lineno)

                visible_line_to_row_col[y] = (lineno, horizontal_scroll)

                # Copy margin and actual line.
                x = 0
                x, y = copy_line(line, lineno, x, y, is_input=True)

                lineno += 1
                y += 1
            return y

        copy()

        def cursor_pos_to_screen_pos(row: int, col: int) -> Point:
            " Translate row/col from UIContent to real Screen coordinates. "
            try:
                y, x = rowcol_to_yx[row, col]
            except KeyError:
                # Normally this should never happen. (It is a bug, if it happens.)
                # But to be sure, return (0, 0)
                return Point(x=0, y=0)

                # raise ValueError(
                #     'Invalid position. row=%r col=%r, vertical_scroll=%r, '
                #     'horizontal_scroll=%r, height=%r' %
                #     (row, col, vertical_scroll, horizontal_scroll, write_position.height))
            else:
                return Point(x=x, y=y)

        # Set cursor and menu positions.
        if ui_content.cursor_position:
            screen_cursor_position = cursor_pos_to_screen_pos(
                ui_content.cursor_position.y, ui_content.cursor_position.x
            )

            if has_focus:
                new_screen.set_cursor_position(self, screen_cursor_position)

                if always_hide_cursor:
                    new_screen.show_cursor = False
                else:
                    new_screen.show_cursor = ui_content.show_cursor

                self._highlight_digraph(new_screen)

            if highlight_lines:
                self._highlight_cursorlines(
                    new_screen,
                    screen_cursor_position,
                    xpos,
                    ypos,
                    width,
                    write_position.height,
                )

        # Draw input characters from the input processor queue.
        if has_focus and ui_content.cursor_position:
            self._show_key_processor_key_buffer(new_screen)

        # Set menu position.
        if ui_content.menu_position:
            new_screen.set_menu_position(
                self,
                cursor_pos_to_screen_pos(
                    ui_content.menu_position.y, ui_content.menu_position.x
                ),
            )

        # Update output screen height.
        new_screen.height = max(new_screen.height, ypos + write_position.height)

        return visible_line_to_row_col, rowcol_to_yx

    def _fill_bg(
            self, screen: Screen, write_position: WritePosition, erase_bg: bool
    ) -> None:
        """
        Erase/fill the background.
        (Useful for floats and when a `char` has been given.)
        """
        char: Optional[str]
        if callable(self.char):
            char = self.char()
        else:
            char = self.char

        if erase_bg or char:
            wp = write_position
            char_obj = _CHAR_CACHE[char or " ", ""]

            for y in range(wp.ypos, wp.ypos + wp.height):
                row = screen.data_buffer[y]
                for x in range(wp.xpos, wp.xpos + wp.width):
                    row[x] = char_obj

    def _apply_style(
            self, new_screen: Screen, write_position: WritePosition, parent_style: str
    ) -> None:

        # Apply `self.style`.
        style = parent_style + " " + to_str(self.style)

        new_screen.fill_area(write_position, style=style, after=False)

        # Apply the 'last-line' class to the last line of each Window. This can
        # be used to apply an 'underline' to the user control.
        wp = WritePosition(
            write_position.xpos,
            write_position.ypos + write_position.height - 1,
            write_position.width,
            1,
        )
        new_screen.fill_area(wp, "class:last-line", after=True)

    def _highlight_digraph(self, new_screen: Screen) -> None:
        """
        When we are in Vi digraph mode, put a question mark underneath the
        cursor.
        """
        digraph_char = self._get_digraph_char()
        if digraph_char:
            cpos = new_screen.get_cursor_position(self)
            new_screen.data_buffer[cpos.y][cpos.x] = _CHAR_CACHE[
                digraph_char, "class:digraph"
            ]

    def _show_key_processor_key_buffer(self, new_screen: Screen) -> None:
        """
        When the user is typing a key binding that consists of several keys,
        display the last pressed key if the user is in insert mode and the key
        is meaningful to be displayed.
        E.g. Some people want to bind 'jj' to escape in Vi insert mode. But the
             first 'j' needs to be displayed in order to get some feedback.
        """
        app = get_app()
        key_buffer = app.key_processor.key_buffer

        if key_buffer and prompt_toolkit.layout.containers._in_insert_mode() and not app.is_done:
            # The textual data for the given key. (Can be a VT100 escape
            # sequence.)
            data = key_buffer[-1].data

            # Display only if this is a 1 cell width character.
            if get_cwidth(data) == 1:
                cpos = new_screen.get_cursor_position(self)
                new_screen.data_buffer[cpos.y][cpos.x] = _CHAR_CACHE[
                    data, "class:partial-key-binding"
                ]

    def _highlight_cursorlines(
            self, new_screen: Screen, cpos: Point, x: int, y: int, width: int, height: int
    ) -> None:
        """
        Highlight cursor row/column.
        """
        cursor_line_style = " class:cursor-line "
        cursor_column_style = " class:cursor-column "

        data_buffer = new_screen.data_buffer

        # Highlight cursor line.
        if self.cursorline():
            row = data_buffer[cpos.y]
            for x in range(x, x + width):
                original_char = row[x]
                row[x] = _CHAR_CACHE[
                    original_char.char, original_char.style + cursor_line_style
                ]

        # Highlight cursor column.
        if self.cursorcolumn():
            for y2 in range(y, y + height):
                row = data_buffer[y2]
                original_char = row[cpos.x]
                row[cpos.x] = _CHAR_CACHE[
                    original_char.char, original_char.style + cursor_column_style
                ]

        # Highlight color columns
        colorcolumns = self.colorcolumns
        if callable(colorcolumns):
            colorcolumns = colorcolumns()

        for cc in colorcolumns:
            assert isinstance(cc, ColorColumn)
            column = cc.position

            if column < x + width:  # Only draw when visible.
                color_column_style = " " + cc.style

                for y2 in range(y, y + height):
                    row = data_buffer[y2]
                    original_char = row[column + x]
                    row[column + x] = _CHAR_CACHE[
                        original_char.char, original_char.style + color_column_style
                    ]

    def _copy_margin(
            self,
            margin_content: UIContent,
            new_screen: Screen,
            write_position: WritePosition,
            move_x: int,
            width: int,
    ) -> None:
        """
        Copy characters from the margin screen to the real screen.
        """
        xpos = write_position.xpos + move_x
        ypos = write_position.ypos

        margin_write_position = WritePosition(xpos, ypos, width, write_position.height)
        self._copy_body(margin_content, new_screen, margin_write_position, 0, width)

    def _scroll(self, ui_content: UIContent, width: int, height: int) -> None:
        """
        Scroll body. Ensure that the cursor is visible.
        """
        if self.wrap_lines():
            func = self._scroll_when_linewrapping
        else:
            func = self._scroll_without_linewrapping

        func(ui_content, width, height)

    def _scroll_when_linewrapping(
            self, ui_content: UIContent, width: int, height: int
    ) -> None:
        """
        Scroll to make sure the cursor position is visible and that we maintain
        the requested scroll offset.

        Set `self.horizontal_scroll/vertical_scroll`.
        """
        scroll_offsets_bottom = self.scroll_offsets.bottom
        scroll_offsets_top = self.scroll_offsets.top

        # We don't have horizontal scrolling.
        self.horizontal_scroll = 0

        def get_line_height(lineno: int) -> int:
            return ui_content.get_height_for_line(lineno, width, self.get_line_prefix)

        # When there is no space, reset `vertical_scroll_2` to zero and abort.
        # This can happen if the margin is bigger than the window width.
        # Otherwise the text height will become "infinite" (a big number) and
        # the copy_line will spend a huge amount of iterations trying to render
        # nothing.
        if width <= 0:
            self.vertical_scroll = ui_content.cursor_position.y
            self.vertical_scroll_2 = 0
            return

        # If the current line consumes more than the whole window height,
        # then we have to scroll vertically inside this line. (We don't take
        # the scroll offsets into account for this.)
        # Also, ignore the scroll offsets in this case. Just set the vertical
        # scroll to this line.
        line_height = get_line_height(ui_content.cursor_position.y)
        if line_height > height - scroll_offsets_top:
            # Calculate the height of the text before the cursor (including
            # line prefixes).
            text_before_height = ui_content.get_height_for_line(
                ui_content.cursor_position.y,
                width,
                self.get_line_prefix,
                slice_stop=ui_content.cursor_position.x,
            )

            # Adjust scroll offset.
            self.vertical_scroll = ui_content.cursor_position.y
            self.vertical_scroll_2 = min(
                text_before_height - 1,  # Keep the cursor visible.
                line_height
                - height,  # Avoid blank lines at the bottom when scolling up again.
                self.vertical_scroll_2,
            )
            self.vertical_scroll_2 = max(
                0, text_before_height - height, self.vertical_scroll_2
            )
            return
        else:
            self.vertical_scroll_2 = 0

        # Current line doesn't consume the whole height. Take scroll offsets into account.
        def get_min_vertical_scroll() -> int:
            # Make sure that the cursor line is not below the bottom.
            # (Calculate how many lines can be shown between the cursor and the .)
            used_height = 0
            prev_lineno = ui_content.cursor_position.y

            for lineno in range(ui_content.cursor_position.y, -1, -1):
                used_height += get_line_height(lineno)

                if used_height > height - scroll_offsets_bottom:
                    return prev_lineno
                else:
                    prev_lineno = lineno
            return 0

        def get_max_vertical_scroll() -> int:
            # Make sure that the cursor line is not above the top.
            prev_lineno = ui_content.cursor_position.y
            used_height = 0

            for lineno in range(ui_content.cursor_position.y - 1, -1, -1):
                used_height += get_line_height(lineno)

                if used_height > scroll_offsets_top:
                    return prev_lineno
                else:
                    prev_lineno = lineno
            return prev_lineno

        def get_topmost_visible() -> int:
            """
            Calculate the upper most line that can be visible, while the bottom
            is still visible. We should not allow scroll more than this if
            `allow_scroll_beyond_bottom` is false.
            """
            prev_lineno = ui_content.line_count - 1
            used_height = 0
            for lineno in range(ui_content.line_count - 1, -1, -1):
                used_height += get_line_height(lineno)
                if used_height > height:
                    return prev_lineno
                else:
                    prev_lineno = lineno
            return prev_lineno

        # Scroll vertically. (Make sure that the whole line which contains the
        # cursor is visible.
        topmost_visible = get_topmost_visible()

        # Note: the `min(topmost_visible, ...)` is to make sure that we
        # don't require scrolling up because of the bottom scroll offset,
        # when we are at the end of the document.
        self.vertical_scroll = max(
            self.vertical_scroll, min(topmost_visible, get_min_vertical_scroll())
        )
        self.vertical_scroll = min(self.vertical_scroll, get_max_vertical_scroll())

        # Disallow scrolling beyond bottom?
        if not self.allow_scroll_beyond_bottom():
            self.vertical_scroll = min(self.vertical_scroll, topmost_visible)

    def _scroll_without_linewrapping(
            self, ui_content: UIContent, width: int, height: int
    ) -> None:
        """
        Scroll to make sure the cursor position is visible and that we maintain
        the requested scroll offset.

        Set `self.horizontal_scroll/vertical_scroll`.
        """
        cursor_position = ui_content.cursor_position or Point(x=0, y=0)

        # Without line wrapping, we will never have to scroll vertically inside
        # a single line.
        self.vertical_scroll_2 = 0

        if ui_content.line_count == 0:
            self.vertical_scroll = 0
            self.horizontal_scroll = 0
            return
        else:
            current_line_text = fragment_list_to_text(
                ui_content.get_line(cursor_position.y)
            )

        def do_scroll(
                current_scroll: int,
                scroll_offset_start: int,
                scroll_offset_end: int,
                cursor_pos: int,
                window_size: int,
                content_size: int,
        ) -> int:
            " Scrolling algorithm. Used for both horizontal and vertical scrolling. "
            # Calculate the scroll offset to apply.
            # This can obviously never be more than have the screen size. Also, when the
            # cursor appears at the top or bottom, we don't apply the offset.
            scroll_offset_start = int(
                min(scroll_offset_start, window_size / 2, cursor_pos)
            )
            scroll_offset_end = int(
                min(scroll_offset_end, window_size / 2, content_size - 1 - cursor_pos)
            )

            # Prevent negative scroll offsets.
            if current_scroll < 0:
                current_scroll = 0

            # Scroll back if we scrolled to much and there's still space to show more of the document.
            if (
                    not self.allow_scroll_beyond_bottom()
                    and current_scroll > content_size - window_size
            ):
                current_scroll = max(0, content_size - window_size)

            # Scroll up if cursor is before visible part.
            if current_scroll > cursor_pos - scroll_offset_start:
                current_scroll = max(0, cursor_pos - scroll_offset_start)

            # Scroll down if cursor is after visible part.
            if current_scroll < (cursor_pos + 1) - window_size + scroll_offset_end:
                current_scroll = (cursor_pos + 1) - window_size + scroll_offset_end

            return current_scroll

        # When a preferred scroll is given, take that first into account.
        if self.get_vertical_scroll:
            self.vertical_scroll = self.get_vertical_scroll(self)
            assert isinstance(self.vertical_scroll, int)
        if self.get_horizontal_scroll:
            self.horizontal_scroll = self.get_horizontal_scroll(self)
            assert isinstance(self.horizontal_scroll, int)

        # Update horizontal/vertical scroll to make sure that the cursor
        # remains visible.
        offsets = self.scroll_offsets

        self.vertical_scroll = do_scroll(
            current_scroll=self.vertical_scroll,
            scroll_offset_start=offsets.top,
            scroll_offset_end=offsets.bottom,
            cursor_pos=ui_content.cursor_position.y,
            window_size=height,
            content_size=ui_content.line_count,
        )

        if self.get_line_prefix:
            current_line_prefix_width = fragment_list_width(
                to_formatted_text(self.get_line_prefix(ui_content.cursor_position.y, 0))
            )
        else:
            current_line_prefix_width = 0

        self.horizontal_scroll = do_scroll(
            current_scroll=self.horizontal_scroll,
            scroll_offset_start=offsets.left,
            scroll_offset_end=offsets.right,
            cursor_pos=get_cwidth(current_line_text[: ui_content.cursor_position.x]),
            window_size=width - current_line_prefix_width,
            # We can only analyse the current line. Calculating the width off
            # all the lines is too expensive.
            content_size=max(
                get_cwidth(current_line_text), self.horizontal_scroll + width
            ),
        )

    def _mouse_handler(self, mouse_event: MouseEvent) -> None:
        """
        Mouse handler. Called when the UI control doesn't handle this
        particular event.
        """
        if mouse_event.event_type == MouseEventType.SCROLL_DOWN:
            self._scroll_down()
        elif mouse_event.event_type == MouseEventType.SCROLL_UP:
            self._scroll_up()

    def _scroll_down(self) -> None:
        " Scroll window down. "
        info = self.render_info

        if info is None:
            return

        if self.vertical_scroll < info.content_height - info.window_height:
            if info.cursor_position.y <= info.configured_scroll_offsets.top:
                self.content.move_cursor_down()

            self.vertical_scroll += 1

    def _scroll_up(self) -> None:
        " Scroll window up. "
        info = self.render_info

        if info is None:
            return

        if info.vertical_scroll > 0:
            # TODO: not entirely correct yet in case of line wrapping and long lines.
            if (
                    info.cursor_position.y
                    >= info.window_height - 1 - info.configured_scroll_offsets.bottom
            ):
                self.content.move_cursor_up()

            self.vertical_scroll -= 1

    def get_key_bindings(self) -> Optional[KeyBindingsBase]:
        return self.content.get_key_bindings()

    def get_children(self) -> List[Container]:
        return []
