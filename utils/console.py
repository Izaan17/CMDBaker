from enum import Enum
from colorama import Fore


class MessageType(Enum):
    """
    Representation of types of messages.
    """
    ERROR = (Fore.RED, "error")
    NOTICE = (Fore.BLUE, "notice")
    CMD = (Fore.GREEN, "cmd")
    WARNING = (Fore.YELLOW, "warning")
    BAKED = (Fore.GREEN, "baked")
    SHEBANG = (Fore.RED, "shebang")
    INTERPRETER = (Fore.YELLOW, "interpreter")
    PATH = (Fore.GREEN, "path")
    SYMBOL = (Fore.BLUE, "symbol")


def format_msg(msg_type: MessageType) -> str:
    """
    Format a message using the message type specified in the MessageType class.
    :param msg_type: Message type.
    :return: Converted MessageType to color coded string.
    """
    color, text = msg_type.value
    return f"[{color}{text}{Fore.RESET}]"


def confirm(prompt: str, default: bool = None) -> bool:
    """
    Ask for yes/no confirmation.
    :param prompt: Question to ask.
    :param default: Default response if user hits enter (None=must choose).
    :return: User response.
    """
    yes_choices = ["y", "yes"]
    no_choices = ["n", "no"]

    if default is True:
        prompt += " [Y/n] "
    elif default is False:
        prompt += " [y/N] "
    else:
        prompt += " [y/n] "

    while True:
        choice = input(prompt).lower().strip()

        if not choice and default is not None:
            return default
        if choice in yes_choices:
            return True
        if choice in no_choices:
            return False
