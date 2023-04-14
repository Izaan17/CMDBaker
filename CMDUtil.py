from colorama import Fore


def error_msg():
    return f"[{Fore.RED}error{Fore.RESET}]"

def notice_msg():
    return f"[{Fore.BLUE}notice{Fore.RESET}]"

def listed_cmd():
    return f"[{Fore.GREEN}cmd{Fore.RESET}]"

def baked_cmd():
    return f"[{Fore.GREEN}baked{Fore.RESET}]"