import os
from utils.console import format_msg, MessageType


def get_path(prompt: str, check_if_exists: bool = False, create: bool = False) -> str:
    """
    Gets a path from user input with optional validation and creation.
    :param prompt: The prompt that is displayed to the user.
    :param check_if_exists: Checks if the path exists before returning the path.
    :param create: Creates the path if the user specified path does not exist.
    :return:
    """
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
