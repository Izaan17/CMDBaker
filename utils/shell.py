import os
from utils.console import MessageType, format_msg

def add_path_to_terminal(main_path: str) -> None:
    """Add the given path to the shell's RC file."""
    current_shell = os.environ['SHELL'].split("/")[-1]
    path_string = f"export PATH=$PATH:{main_path}\n"
    rc_path = f"{os.path.expanduser('~')}/.{current_shell}rc"

    try:
        with open(rc_path, 'a+') as file:
            file.seek(0)
            if path_string not in file.read():
                file.write(path_string)
    except IOError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to update shell config: {e}")

def chmod_executable(path: str) -> None:
    """Make a file executable."""
    try:
        os.chmod(path, 0o755)
    except OSError as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to make file executable: {e}")