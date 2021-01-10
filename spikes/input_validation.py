from prompt_toolkit import prompt, HTML
from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input contains non-numeric characters',
                                  cursor_position=i)


def is_number(text):
    return text.isdigit()


def bottom_toolbar():
    return HTML('This is a <b><style bg="ansired">Toolbar</style></b>!')
    # By default, the toolbar has the reversed style,
    # which is why we are setting the background instead of the foreground.


if __name__ == '__main__':
    number = int(prompt('Give a number: ', validator=NumberValidator(), validate_while_typing=False))
    print('You said: %i' % number)

    validator = Validator.from_callable(
        is_number,
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)

    number = int(prompt('Give a number: ', validator=validator, validate_while_typing=False))
    print('You said: %i' % number)

    text = prompt('> ', bottom_toolbar=bottom_toolbar)
    print('You said: %s' % text)

# more info https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html#input-validation
