from colorama import Fore


def error_msg():
    return f"[{Fore.RED}error{Fore.RESET}]"

def notice_msg():
    return f"[{Fore.BLUE}notice{Fore.RESET}]"

def listed_cmd():
    return f"[{Fore.GREEN}cmd{Fore.RESET}]"

def baked_cmd():
    return f"[{Fore.GREEN}baked{Fore.RESET}]"

def confirmation(prompt):
    yes_choices = ["y", "yes"]
    no_choices = ["n", "no"]
    while True:
        choice = input(prompt).lower()
        if choice in yes_choices:
            return True
        elif choice in no_choices:
            return False
        else:
            continue