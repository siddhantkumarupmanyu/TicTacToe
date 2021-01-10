from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls, Style
from pygments.lexers.html import HtmlLexer
from pygments.styles import get_style_by_name

if __name__ == '__main__':
    text = prompt('Give me some input: ')
    print(f"You said: {text}")

    # https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html#the-promptsession-object
    # advantages over simple prompt
    # The input history will be kept between consecutive prompt() calls.
    # passing arguments(highlighting, completion, etc…) at a single place not on every prompt call

    # Create prompt object.
    session = PromptSession()

    # Do multiple input calls.
    text1 = session.prompt()
    text2 = session.prompt()

    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer))
    print('You said: %s' % text)

    style = style_from_pygments_cls(get_style_by_name('monokai'))
    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer), style=style,
                  include_default_pygments_style=False)
    print('You said: %s' % text)

    style = Style.from_dict({
        # User input (default text).
        '': '#ff0066',

        # Prompt.
        'username': '#884444',
        'at': '#00aa00',
        'colon': '#0000aa',
        'pound': '#00aa00',
        'host': '#00ffff bg:#444400',
        'path': 'ansicyan underline',
    })

    # message is a formatted text; see formatted.py
    message = [
        ('class:username', 'john'),
        ('class:at', '@'),
        ('class:host', 'localhost'),
        ('class:colon', ':'),
        ('class:path', '/user/john'),
        ('class:pound', '# '),
    ]

    text = prompt(message, style=style)

