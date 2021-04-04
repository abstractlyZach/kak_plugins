import os
import pipes

# TODO: how do I test this file??


def get_clipboard_command() -> str:
    clipboard = os.getenv("CLIPBOARD")
    if clipboard is None:
        raise EnvironmentError("CLIPBOARD is not defined")
    else:
        return clipboard


default_clipboard_command = get_clipboard_command()


def write_to_clipboard(
    message: str, clipboard_command: str = default_clipboard_command
) -> None:
    template = pipes.Template()
    # takes in input and writes no output
    template.append(clipboard_command, "-.")
    with template.open("tempfile", "w") as clipboard:  # won't actually open a file
        clipboard.write(message)