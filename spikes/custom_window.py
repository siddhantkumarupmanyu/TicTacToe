from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Window, FormattedTextControl, Layout, WindowAlign

from spikes.test_window import TestWindow

rootLayout = TestWindow(content=FormattedTextControl(text='Hello world\nhello world'), align=WindowAlign.CENTER)

kb = KeyBindings()


@kb.add('c-q')
def exit_(event):
    event.app.exit()


if __name__ == '__main__':
    app = Application(layout=Layout(rootLayout), full_screen=True, key_bindings=kb)
    app.run()
