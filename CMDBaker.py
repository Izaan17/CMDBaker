import argparse
import os

import CMDBakerSetup
from CMDBakerSetup import Config, home


def add_path_to_terminal(main_path):
    # Get Shells name
    current_shell = os.environ['SHELL'].split("/")[-1]
    path_string = f"\nexport PATH=$PATH:{main_path}"
    with open(f"{home}/.{current_shell}rc", 'a+') as file:
        file.seek(0)
        found = False
        lines = file.readlines()
        for line in lines:
            # Check if previously was writen else it will write again.
            if path_string in line:
                found = True
        if not found:
            file.write(path_string)


def chmod(full_path):
    os.system(f"chmod +x {full_path}")


def create_command(command_name, baked_command, starting_location=None):
    if starting_location is None:
        starting_location = baked_commands_path
    full_path = f"{starting_location}/{command_name}"
    with open(full_path, 'w') as command_file:
        command_file.write(baked_command)
    chmod(full_path)
    add_path_to_terminal(starting_location)


def edit_command(command_name):
    full_path = f"{baked_commands_path}/{command_name}"
    if os.path.exists(full_path):
        with open(full_path, 'r') as old_command_file:
            contents = old_command_file.read()
            split_contents = contents.split()
            old_shebang = split_contents[0]
            old_interpreter = split_contents[1]
            old_source = split_contents[2]
            print(contents)
            new_command_name = input("Command name (leave empty for same one): ").strip()
            new_command_name = new_command_name if new_command_name != "" else command_name
            shebang = input("Shebang (leave empty for same one): ").strip()
            shebang = shebang if shebang != "" else old_shebang
            source = input("Source (leave empty for same one): ").strip()
            source = source if source != "" else old_source
            interpreter = input("Interpreter (leave empty for same one): ").strip()
            interpreter = interpreter if interpreter != "" else old_interpreter
            baked_command = bake_command(source, interpreter, shebang)
            create_command(new_command_name, baked_command=baked_command)
    else:
        print(f"[-] '{full_path}' does not exist.")


def view_command(command_name):
    full_path = f"{baked_commands_path}/{command_name}"
    if os.path.exists(full_path):
        with open(full_path, 'r') as old_command_file:
            contents = old_command_file.read()
            print(contents)


def delete_command(command_name):
    full_path = f"{baked_commands_path}/{command_name}"
    if os.path.exists(full_path):
        os.remove(full_path)
    else:
        print(f"[-] '{full_path}' does not exist.")


def bake_command(source, shebang=None, interpreter=None):
    if shebang is None:
        shebang = "#!/bin/zsh"
    if interpreter is None:
        interpreter = "python3"
    command_string = "$@"
    bake_string = [interpreter, source, command_string]
    full_script = f"""{shebang}\n{' '.join(bake_string)}"""
    return full_script


def list_commands():
    baked_commands = os.listdir(baked_commands_path)
    for command in baked_commands:
        if command != ".DS_Store":
            print(command)


config = Config(CMDBakerSetup.config_location)
config_data = config.load_config()
baked_commands_path = config_data['main_path']
is_baked = config_data['is_baked']
parser = argparse.ArgumentParser(prog="CMDBaker",
                                 description="Easily bake new commands.",
                                 epilog="Made by Izaan")
parser.add_argument("command_name", help="The commands name.", type=str, nargs='?')
parser.add_argument("source", help="The python script to run.", type=str, nargs='?')
parser.add_argument("-i", "--interpreter", help="Which version of python.", type=str)
parser.add_argument("-s", "--shebang", help="The top of the file.", type=str)
parser.add_argument("-l", "--list", help="Lists all the commands created with bake.", action="store_true")
parser.add_argument("-d", "--delete", help="Delete baked commands.")
parser.add_argument("-e", "--edit", help="Edit baked commands.")
parser.add_argument("-v", "--view", help="View contents of baked commands.")
args = parser.parse_args()

if args.list:
    list_commands()
    quit(0)

if args.delete:
    delete_command(args.delete)
    quit(0)

if args.edit:
    edit_command(args.edit)
    quit(0)

if args.view:
    view_command(args.view)
    quit(0)
if args.command_name and args.source:
    command_name = args.command_name.strip()
    # Bake ourselves first to allow access to bake in the terminal
    if not is_baked:
        self_baked_command = bake_command(source=__file__)
        print("[+] Baked self to make it easier!")
        print("[+] You can now bake new commands using the bake command!")
        create_command("bake", self_baked_command, starting_location=CMDBakerSetup.folder_location)
        # Set that we are baked
        config.append_config("is_baked", True)

    create_command(command_name=command_name,
                   baked_command=bake_command(source=args.source, interpreter=args.interpreter, shebang=args.shebang))
    print(f"Baked '{command_name}'")
else:
    parser.print_help()
    quit(-1)
