from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import Layout, HSplit, VSplit, D, Window, FormattedTextControl, WindowAlign, VerticalAlign
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import MenuContainer, MenuItem, Frame, Label


def do_exit():
    get_app().exit()


scoreBoard = HSplit([
    Label(text="Player 1 Points = 0"),
    Label(text="Player 2 Points = 6"),
], align="CENTER")

ticTacToeWindow = HSplit(
    [
        Window(
            content=FormattedTextControl("x | x | x \n x | x | x \n x | x | x", focusable=True),
            align=WindowAlign.CENTER,
            height=D(weight=1)
        )
    ], align=VerticalAlign.CENTER
)

tempContainer = VSplit([
    Frame(body=ticTacToeWindow, title="Tic tac toe", width=D(weight=2), height=D()),
    Frame(body=scoreBoard, title="ScoreBoard", width=D(weight=1))
],
    height=D()
)

root_container = MenuContainer(
    body=tempContainer,
    menu_items=[
        MenuItem(
            "File",
            children=[
                MenuItem("New"),
                MenuItem("Exit", handler=do_exit),
            ]
        )
    ]
)

# Global key bindings.
bindings = KeyBindings()
bindings.add("tab")(focus_next)
bindings.add("s-tab")(focus_previous)


def exit_():
    get_app().exit()


style = Style.from_dict(
    {
        "window.border": "#888888",
        "shadow": "bg:#222222",
        "menu-bar": "bg:#aaaaaa #888888",
        "menu-bar.selected-item": "bg:#ffffff #000000",
        "menu": "bg:#888888 #ffffff",
        "menu.border": "#aaaaaa",
        "window.border shadow": "#444444",
        "focused  button": "bg:#880000 #ffffff noinherit",
        # Styling for Dialog widgets.
        "button-bar": "bg:#aaaaff",
    }
)

application = Application(
    layout=Layout(root_container),
    key_bindings=bindings,
    style=style,
    mouse_support=True,
    full_screen=True,
)


def run():
    application.run()


def startApp():
    run()


if __name__ == '__main__':
    startApp()
