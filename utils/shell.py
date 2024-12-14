import os

from utils.console import MessageType, format_msg


def add_path_to_terminal(main_path: str) -> None:
    """
    Add the given path to the shell's RC (runtime configuration) file.

    :param main_path: The path to be added to the shell's RC file.
    :return: None
    """
    try:
        current_shell = get_current_shell_name()
        rc_path = os.path.expanduser(f"~/.{current_shell}rc")
        path_string = f"export PATH=$PATH:{main_path}\n"

        # Append the path to the RC file if it doesn't already exist
        with open(rc_path, "a+") as file:
            file.seek(0)
            if path_string not in file.read():
                file.write(path_string)
    except IOError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to update shell config: {e}")


def get_current_shell_path() -> str:
    """
    Get the full path of the current shell.

    :return: The path of the current shell.
    """
    return os.environ.get("SHELL", "")


def get_current_shell_name() -> str:
    """
    Get the name of the current shell (e.g., 'bash', 'zsh').

    :return: The name of the current shell.
    """
    return os.path.basename(get_current_shell_path())


def chmod_executable(path: str) -> None:
    """
    Make the specified file executable by changing its permissions.

    :param path: The path of the file to make executable.
    :return: None
    """
    try:
        os.chmod(path, 0o755)
    except OSError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to make file executable: {e}")


def open_fs(name: str) -> None:
    """
    Open the specified file, directory, or application via the operating system.

    :param name: The name of the file, directory, or application to open.
    :return: None
    """
    os.system(f"open {name}")
