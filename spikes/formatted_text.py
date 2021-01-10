from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.styles import Style

if __name__ == '__main__':
    print_formatted_text(HTML('<b>This is bold</b>'))
    print_formatted_text(HTML('<i>This is italic</i>'))
    print_formatted_text(HTML('<u>This is underlined</u>'))

    # Colors from the ANSI palette.
    print_formatted_text(HTML('<ansired>This is red</ansired>'))
    print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))

    # Named colors (256 color palette, or true color, depending on the output).
    print_formatted_text(HTML('<skyblue>This is sky blue</skyblue>'))
    print_formatted_text(HTML('<seagreen>This is sea green</seagreen>'))
    print_formatted_text(HTML('<violet>This is violet</violet>'))

    # Both foreground and background colors can also be specified setting the fg and bg attributes of any HTML tag:
    # Colors from the ANSI palette.
    print_formatted_text(HTML('<aaa fg="ansiwhite" bg="ansigreen">White on green</aaa>'))

    # Underneath, all HTML tags are mapped to classes from a stylesheet, so you can assign a style for a custom tag.
    style = Style.from_dict({
        'aaa': '#ff0066',
        'bbb': '#44ff00 italic',
    })

    print_formatted_text(HTML('<aaa>Hello</aaa> <bbb>world</bbb>!'), style=style)

    # A useful function to know about is to_formatted_text().
    # This ensures that the given input is valid formatted text.
    # While doing so, an additional style can be applied as well.
    html = HTML('<aaa>Hello</aaa> <bbb>world</bbb>!')
    text = to_formatted_text(html, style='class:my_html bg:#00ff00 italic')

    print_formatted_text(text)

# for more info https://python-prompt-toolkit.readthedocs.io/en/master/pages/printing_text.html
