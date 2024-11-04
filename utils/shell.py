import os

from utils.console import MessageType, format_msg


def add_path_to_terminal(main_path: str) -> None:
    """
    Add the given path to the shell's RC file.
    :param main_path: Add the main path to the terminals rc file.
    :return: None
    """
    current_shell = get_current_shell_name()
    path_string = f"export PATH=$PATH:{main_path}\n"
    rc_path = f"{os.path.expanduser("~")}/.{current_shell}rc"

    try:
        with open(rc_path, "a+") as file:
            file.seek(0)
            if path_string not in file.read():
                file.write(path_string)
    except IOError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to update shell config: {e}")


def get_current_shell_path() -> str:
    return os.environ["SHELL"]

def get_current_shell_name() -> str:
    return get_current_shell_path().split("/")[-1]


def chmod_executable(path: str) -> None:
    """
    Make a file executable.
    :param path: The path to make executable.
    :return: None
    """
    try:
        os.chmod(path, 0o755)
    except OSError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to make file executable: {e}")


def open_fs(name: str) -> None:
    """
    Opens the specified file, directory or application via the operating system.
    :param name: Name of application, file, or directory.
    :return: None
    """
    os.system(f"open {name}")
