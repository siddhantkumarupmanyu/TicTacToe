"""
A simple example of a few buttons and click handlers.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    VSplit,
)
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea

state = 2


# Event handlers for all the buttons.
def button1_clicked():
    state = 1
    text_area.text = "Button 1 clicked"


def button2_clicked():
    state = 2
    # print(state)
    text_area.text = "Button 2 clicked"


def button3_clicked():
    text_area.text = "Button 3 clicked"


def exit_clicked():
    get_app().exit()


# All the widgets for the UI.
button1 = Button("Button 1", handler=button1_clicked)
button2 = Button("Button 2", handler=button2_clicked)
button3 = Button("Button 3", handler=button3_clicked)
button4 = Button("Button 1.1", handler=button1_clicked)
button5 = Button("Button 1.2", handler=button2_clicked)
button6 = Button("Button 1.3", handler=button3_clicked)
button7 = Button("Exit", handler=exit_clicked)
text_area = TextArea(focusable=True)

# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
root_container = Box(
    HSplit(
        [
            Label(text="Press `Tab` to move the focus."),
            VSplit(
                [
                    ConditionalContainer(
                        content=Frame(
                            Box(
                                body=HSplit([button1, button2, button3, button7], padding=1),
                                padding=1,
                                style="class:left-pane",
                            )
                        ),
                        filter=Condition(lambda: True if (state == 1) else False),
                    ),
                    ConditionalContainer(
                        content=Frame(
                            Box(
                                body=HSplit([button4, button5, button6, button7], padding=1),
                                padding=1,
                                style="class:left-pane",
                            )
                        ),
                        filter=Condition(lambda: True if (state == 2) else False),
                    ),
                ]
            ),
        ],
    ),
)

layout = Layout(container=root_container, focused_element=button1)

# Key bindings.
kb = KeyBindings()
kb.add("tab")(focus_next)
kb.add("s-tab")(focus_previous)
kb.add("down")(focus_next)
kb.add("up")(focus_previous)

# Styling.
style = Style(
    [
        ("button", "#00ff00"),
        ("button-arrow", "bg:#00ff00"),
        ("button focused", "bg:#00ff00"),
        ("text-area focused", "bg:#ff0000"),
        ("text-area", "bg:#ff0000"),
    ]
)

# Build a main application object.
application = Application(layout=layout, key_bindings=kb, style=None, full_screen=True)


def main():
    application.run()


if __name__ == "__main__":
    main()

# not working as supposed i think
