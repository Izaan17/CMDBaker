import os
import time
from typing import Optional

from utils.console import MessageType, format_msg
from utils.shell import chmod_executable, get_current_shell_path


class CommandHandler:
    def __init__(self, commands_path: str, verbose: bool = False) -> None:
        """
        Initializes the CommandHandler instance.

        :param commands_path: Directory path where commands are stored.
        :param verbose: Flag to enable verbose output.
        """
        self.commands_path = commands_path
        self.verbose = verbose

    def create_command(self, command_name: str, baked_command: str, starting_location: Optional[str] = None) -> None:
        """
        Create a new baked command.

        :param command_name: The name of the command.
        :param baked_command: The command's compiled string.
        :param starting_location: Optional path where the command will be created. Defaults to `self.commands_path`.
        """
        location = starting_location or self.commands_path
        full_path = os.path.join(location, command_name)

        try:
            with open(full_path, "w") as command_file:
                command_file.write(baked_command)
            chmod_executable(full_path)
        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to create command: {e}")

    def edit_command(self, command_name: str) -> None:
        """
        Edit an existing command.

        :param command_name: The name of the command to be edited.
        """
        full_path = self.get_command_path(command_name)

        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(full_path, "r") as file:
                contents = file.read()

            # Display current command and prompt for updates
            print(contents)
            new_name = input(f"Command name (leave empty for '{command_name}'): ").strip() or command_name
            parts = contents.split()
            new_shebang = input(f"Shebang (leave empty for '{parts[0]}'): ").strip() or parts[0]
            new_interpreter = input(f"Interpreter (leave empty for '{parts[1]}'): ").strip() or parts[1]
            new_source = input(f"Source (leave empty for '{parts[2]}'): ").strip() or parts[2]

            # Create updated command
            baked_command = self.bake_command(new_source, new_shebang, new_interpreter)
            self.create_command(new_name, baked_command)

            # Delete old command if name changed
            if new_name != command_name:
                self.delete_command(command_name)

        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to edit command: {e}")

    def command_exists(self, command_name: str) -> bool:
        """
        Check if a command exists.

        :param command_name: The name of the command to check.
        :return: True if the command exists, otherwise False.
        """
        return os.path.exists(self.get_command_path(command_name))

    def view_command(self, command_name: str) -> None:
        """
        View the contents of a command.

        :param command_name: The name of the command to view.
        """
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(self.get_command_path(command_name), "r") as file:
                content = file.read().splitlines()
                shebang, command = content[0], content[1].split()

                # Set a fixed width for formatted output
                field_width = 25
                print(f"{format_msg(MessageType.SHEBANG):<{field_width}} {shebang}")
                print(f"{format_msg(MessageType.INTERPRETER):<{field_width}} {command[0]}")
                print(f"{format_msg(MessageType.PATH):<{field_width}} {command[1]}")
                print(f"{format_msg(MessageType.SYMBOL):<{field_width}} {command[2]}")
        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to read command: {e}")

    def list_commands(self) -> None:
        """
        List all available baked commands.

        :return: None
        """
        try:
            # List all non-hidden files in the commands directory
            commands = [cmd for cmd in os.listdir(self.commands_path) if not cmd.startswith(".")]

            # Define column widths for consistent formatting
            command_width = 15
            path_width = max(len(os.path.join(self.commands_path, cmd)) for cmd in commands)

            for command in commands:
                full_path = os.path.join(self.commands_path, command)
                # Include modification time and path if verbose
                if self.verbose:
                    mod_time = time.ctime(os.path.getmtime(full_path))
                    extra = f" | {full_path:<{path_width}} | {mod_time}"
                else:
                    extra = ""
                print(f"{format_msg(MessageType.CMD)} {command:<{command_width}} {extra}")
        except OSError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to list commands: {e}")

    def delete_command(self, command_name: str) -> None:
        """
        Delete a specified command.

        :param command_name: The name of the command to delete.
        """
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            os.remove(self.get_command_path(command_name))
        except OSError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to delete command: {e}")

    def get_command_path(self, command_name: str) -> str:
        """
        Get the full path for a command.

        :param command_name: The command name to get the path for.
        :return: Full path to the command.
        """
        return os.path.join(self.commands_path, command_name)

    def get_command_source(self, command_name: str) -> Optional[str]:
        """
        Retrieve the source file path of a command.

        :param command_name: The name of the command.
        :return: Path of the command's source, or None if the command doesn't exist.
        """
        if not self.command_exists(command_name):
            return None

        with open(self.get_command_path(command_name), "r") as file:
            return file.read().split()[2]

    @staticmethod
    def bake_command(source: str, shebang: Optional[str] = None, interpreter: Optional[str] = None) -> str:
        """
        Create the command string.

        :param source: The source of the Python file.
        :param shebang: Optional shebang for the file (defaults to the current shell).
        :param interpreter: Optional interpreter (defaults to 'python3').
        :return: The compiled string for the baked command.
        """
        shebang = shebang or "#!" + get_current_shell_path()
        interpreter = interpreter or "python3"
        return f"{shebang}\n{interpreter} {source} $@"
