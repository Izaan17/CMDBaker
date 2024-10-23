import os
from utils.console import format_msg, MessageType


def get_path(prompt, check_if_exists=False, create=False):
    """Gets a path from user input with optional validation and creation."""
    while True:
        path = input(prompt).strip()

        if check_if_exists and not os.path.exists(path):
            print(format_msg(MessageType.ERROR), "Path does not exist")
            continue

        if create:
            try:
                os.makedirs(path, exist_ok=True)
            except PermissionError:
                print(format_msg(MessageType.ERROR), "Cannot create directory")
                continue

        return path
