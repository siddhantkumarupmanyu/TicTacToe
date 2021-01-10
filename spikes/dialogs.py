from prompt_toolkit.shortcuts import message_dialog, input_dialog, yes_no_dialog, button_dialog

if __name__ == '__main__':
    message_dialog(
        title='Example dialog window',
        text='Do you want to continue?\nPress ENTER to quit.').run()

    text = input_dialog(
        title='Input dialog example',
        text='Please type your name:').run()

    result = yes_no_dialog(
        title='Yes/No dialog example',
        text='Do you want to confirm?').run()

    result = button_dialog(
        title='Button dialog example',
        text='Do you want to confirm?',
        buttons=[
            ('Yes', True),
            ('No', False),
            ('Maybe...', None)
        ],
    ).run()


# more info https://python-prompt-toolkit.readthedocs.io/en/master/pages/dialogs.html
