import logging
import os
import subprocess

# TODO: how do I test this file??


def get_clipboard_command() -> str:
    clipboard = os.getenv("CLIPBOARD")
    if clipboard is None:
        raise EnvironmentError("CLIPBOARD is not defined")
    else:
        return clipboard


def write_to_clipboard(message: str, clipboard_command: str) -> None:
    logging.debug(f"Clipboard is {clipboard_command}")
    subprocess.run(clipboard_command, input=message, text=True)  # noqa: S603
    logging.debug(f"writing '{message}' to clipboard")
