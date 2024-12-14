import argparse
import os

import setup
from commands.handler import CommandHandler
from config import Config
from constants import FOLDER_LOCATION, CONFIG_LOCATION, fetch_latest_version
from utils.console import MessageType, format_msg, confirm
from utils.shell import add_path_to_terminal, open_fs, get_current_shell_path


def get_args() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        prog="CMDBaker",
        description="Easily bake new commands.",
        epilog="Made by Izaan"
    )

    # Positional arguments
    parser.add_argument("command_name", help="The command's name", type=str, nargs='?')
    parser.add_argument("source", help="The python script to run", type=argparse.FileType(), nargs='?')

    # Optional Arguments
    parser.add_argument("-i", "--interpreter", help="Which version of Python to use")
    parser.add_argument("-s", "--shebang", help="The shebang line to prepend to the script")
    parser.add_argument("-vb", "--verbose", help="Print out more details in each command", action="store_true")
    parser.add_argument("-vc", "--view", help="View contents of a baked command")
    parser.add_argument("-e", "--edit", help="Edit a baked command")
    parser.add_argument("-d", "--delete", help="Delete a baked command")
    parser.add_argument("-l", "--list", help="List all baked commands", action="store_true")
    parser.add_argument("-p", "--print", help="Print the main path", action="store_true")

    # Marketplace Arguments (grouped under a subparser)
    marketplace_parser = parser.add_argument_group("Marketplace Operations")
    marketplace_parser.add_argument("-m", "--marketplace", help="Interact with the Python script marketplace")
    marketplace_parser.add_argument("-ms", "--marketplace-search", help="Search for scripts in the marketplace")
    marketplace_parser.add_argument("-mi", "--marketplace-install", help="Install a script from the marketplace")
    marketplace_parser.add_argument("-mu", "--marketplace-update", help="Update a script from the marketplace")

    # Config Arguments
    parser.add_argument("-c", "--config", help="Redo setup process", action="store_true")
    parser.add_argument("-em", "--main", help="Edit main path")
    parser.add_argument("-in", "--into", help="CD into baked commands directory")
    parser.add_argument("-es", "--edit-script", help="Edit the baked command's script")

    # Version and Update Handling
    parser.add_argument("-u", "--update", help="Update from git", action="store_true")
    parser.add_argument("-fu", "--force-update", help="Force update from git", action="store_true")
    parser.add_argument("-v", "--version", help="Outputs current version", action="store_true")

    return parser.parse_args()


def update_cmd_baker(config, latest_version) -> None:
    """Update CMD Baker from git."""
    print(f"{format_msg(MessageType.NOTICE)} Updating...")
    current_dir = os.getcwd()
    command_origin = os.path.dirname(__file__)

    # Ensure we're in the correct directory for git operations
    os.chdir(command_origin)
    os.system("git pull")  # Perform the update via git
    os.chdir(current_dir)  # Restore the original working directory

    # Update config with the new version
    config.append_config("version", latest_version)


def main() -> None:
    """Main function to handle command-line operations."""
    setup.main()  # Initialize settings

    # Load configuration
    config = Config(CONFIG_LOCATION)
    config_data = config.load_config()
    version = config_data.get("version")
    commands_path = config_data["main_path"]
    bake_command_file_path = os.path.join(FOLDER_LOCATION, "bake")

    # Add the command path to terminal
    add_path_to_terminal(commands_path)

    # Parse command-line arguments
    args = get_args()

    # Initialize command handler
    handler = CommandHandler(commands_path, args.verbose)

    # Self-baking check (if 'bake' command doesn't exist, bake it)
    if not os.path.exists(bake_command_file_path):
        print(f"{format_msg(MessageType.NOTICE)} Baking self...")
        baked_command = handler.bake_command(__file__)
        handler.create_command("bake", baked_command, FOLDER_LOCATION)
        config.append_config("is_baked", True)
        print(f"{format_msg(MessageType.NOTICE)} You can now use the 'bake' command!")
        return

    # Handle old version issues and update bake file
    if not version:  # User is on an old version of bake
        print(format_msg(MessageType.WARNING), "You are on an old version of bake.")
        print(format_msg(MessageType.NOTICE), "Deleting old bake file.")
        try:
            os.remove(bake_command_file_path)
            print(format_msg(MessageType.NOTICE), "Successfully deleted old bake command.")
            # Update config with the latest version
            config_data["version"] = fetch_latest_version()
            config.write_config(config_data)
            return main()
        except OSError as error:
            print(format_msg(MessageType.ERROR), f"An error occurred deleting the old bake file: {error}")
            print(format_msg(MessageType.NOTICE), f"You can delete it manually located at: {bake_command_file_path}")

    # Handle specific flags like list, delete, update, etc.
    if args.list:
        handler.list_commands()
    elif args.delete:
        handler.delete_command(args.delete)
    elif args.edit:
        handler.edit_command(args.edit)
    elif args.view:
        handler.view_command(args.view)
    elif args.into:
        if handler.command_exists(args.into):
            source = handler.get_command_source(args.into)
            folder = os.path.dirname(source)
            current_shell = get_current_shell_path()
            try:
                os.chdir(folder)
                os.system(current_shell)
            except OSError as error:
                print(format_msg(MessageType.ERROR), f"An error occurred changing directories: {error}")
        else:
            print(format_msg(MessageType.ERROR), f"Command '{args.into}' does not exist")
    elif args.print:
        print(f"{format_msg(MessageType.NOTICE)} {commands_path}")
    elif args.config:
        if confirm("Are you sure you want to redo setup?", default=False):
            os.remove(CONFIG_LOCATION)
    elif args.update:
        # Handle update process
        latest_version = fetch_latest_version()
        if version < latest_version:
            if confirm(f"{format_msg(MessageType.NOTICE)} An update is available. Do you want to update?", True):
                update_cmd_baker(config, latest_version)
        else:
            print(f"{format_msg(MessageType.NOTICE)} No update available.")
    elif args.force_update:
        update_cmd_baker(config, fetch_latest_version())
    elif args.version:
        print(f"{format_msg(MessageType.NOTICE)} Version: {version}")
    elif args.edit_script:
        if handler.command_exists(args.edit_script):
            open_fs(handler.get_command_source(args.edit_script))
        else:
            print(format_msg(MessageType.ERROR), f"Command '{args.edit_script}' does not exist")
    else:
        # Command baking logic
        if args.command_name and args.source:
            command_name = args.command_name.strip().lower()

            if command_name == "bake":
                print(f"{format_msg(MessageType.ERROR)} Command name cannot be 'bake'")
                return

            if handler.command_exists(command_name):
                print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' already exists")
                return

            baked_command = handler.bake_command(args.source.name, args.shebang, args.interpreter)
            handler.create_command(command_name, baked_command)
            print(f"{format_msg(MessageType.CMD)} Baked '{command_name}'")


if __name__ == '__main__':
    main()
