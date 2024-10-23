import argparse
import os
import shutil

from commands.handler import CommandHandler
from config import Config
from constants import FOLDER_LOCATION, CONFIG_LOCATION
from utils.console import MessageType, format_msg, confirm
from utils.shell import add_path_to_terminal
import setup


def get_args() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        prog="CMDBaker",
        description="Easily bake new commands.",
        epilog="Made by Izaan"
    )

    parser.add_argument("command_name", help="The command's name", type=str, nargs='?')
    parser.add_argument("source", help="The python script to run", type=str, nargs='?')
    parser.add_argument("-i", "--interpreter", help="Which version of python")
    parser.add_argument("-s", "--shebang", help="The top of the file")
    parser.add_argument("-l", "--list", help="List all baked commands", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete a baked command")
    parser.add_argument("-e", "--edit", help="Edit a baked command")
    parser.add_argument("-v", "--view", help="View contents of a baked command")
    parser.add_argument("-c", "--config", help="Redo setup process", action="store_true")
    parser.add_argument("-m", "--main", help="Edit main path")
    parser.add_argument("-u", "--update", help="Update from git", action="store_true")
    parser.add_argument("-p", "--print", help="Print main path", action="store_true")
    parser.add_argument("-in", "--into", help="CD into baked commands directory")

    return parser.parse_args()

def update_cmd_baker():
    """Update CMD Baker from git."""
    print(f"{format_msg(MessageType.NOTICE)} Updating...")
    current_dir = os.getcwd()
    command_origin = os.path.dirname(__file__)
    os.chdir(command_origin)
    os.system("git pull")
    os.chdir(current_dir)

def main():
    setup.main() # Init settings

    config = Config(CONFIG_LOCATION)
    config_data = config.load_config()
    version = config_data.get('version')
    commands_path = config_data['main_path']
    bake_command_file_path = os.path.join(FOLDER_LOCATION, "bake")

    # Initialize command handler
    handler = CommandHandler(commands_path)

    # Add path to terminal
    add_path_to_terminal(commands_path)

    args = get_args()

    # Self-baking check
    if not os.path.exists(bake_command_file_path):
        print(f"{format_msg(MessageType.NOTICE)} Baking self...")
        baked_command = handler.bake_command(__file__)
        handler.create_command("bake", baked_command, FOLDER_LOCATION)
        config.append_config("is_baked", True)
        print(f"{format_msg(MessageType.NOTICE)} You can now use the 'bake' command!")
        return

    # Old versions of bake don't have the version key in the config and no longer work so we have to fix it
    if not version:  # User is on old version of bake
        print(format_msg(MessageType.WARNING), "You are on an old version of bake.")
        print(format_msg(MessageType.NOTICE), "Deleting old bake file.")
        try:
            shutil.rmtree(FOLDER_LOCATION)
            print(format_msg(MessageType.NOTICE), "Successfully deleted old bake command.")
            print(format_msg(MessageType.NOTICE), "Rebaking self...")
            return main()
        except OSError as error:
            print(format_msg(MessageType.ERROR), f"An error occurred deleting the old bake folder: {error}")
            print(format_msg(MessageType.NOTICE), f"You can delete it manually located at: {bake_command_file_path}")

    # Handle command line arguments
    if args.into:
        if handler.command_exists(args.into):
            path = handler.get_command_path(args.into)
            with open(path, 'r') as file:
                source = file.read().split()[1]
                folder = os.path.dirname(source)
                current_shell = os.environ['SHELL'].split("/")[-1]
                os.chdir(folder)
                os.system(f"/bin/{current_shell}")
        return

    if args.main:
        if os.path.exists(args.main):
            config.append_config("main_path", args.main)
        else:
            print(f"{format_msg(MessageType.ERROR)} Path '{args.main}' does not exist")
        return

    if args.update:
        update_cmd_baker()
        return

    if args.list:
        handler.list_commands()
        return

    if args.delete:
        handler.delete_command(args.delete)
        return

    if args.edit:
        handler.edit_command(args.edit)
        return

    if args.view:
        handler.view_command(args.view)
        return

    if args.config:
        if confirm("Are you sure you want to redo setup?"):
            os.remove(CONFIG_LOCATION)
        return

    if args.print:
        print(f"{format_msg(MessageType.NOTICE)} {commands_path}")
        return

    if args.command_name and args.source:
        command_name = args.command_name.strip()
        if handler.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' already exists")
            return

        baked_command = handler.bake_command(
            args.source,
            args.shebang,
            args.interpreter
        )
        handler.create_command(command_name, baked_command)
        print(f"{format_msg(MessageType.CMD)} Baked '{command_name}'")


if __name__ == '__main__':
    main()
