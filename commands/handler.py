import os
import time
from typing import Optional

from utils.console import MessageType, format_msg
from utils.shell import chmod_executable, get_current_shell_path


class CommandHandler:
    def __init__(self, commands_path: str, verbose: bool = None) -> None:
        self.commands_path = commands_path
        self.verbose = verbose if verbose else False

    def create_command(self, command_name: str, baked_command: str, starting_location: Optional[str] = None) -> None:
        """
        Create a new baked command.
        :param command_name: The command name to be baked.
        :param baked_command: The compiled version of the baked command.
        :param starting_location: The starting location of the command. *(Used for baking self)*
        :return: None
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
        :param command_name: The command name to be edited.
        :return: None
        """
        full_path = self.get_command_path(command_name)
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(full_path, "r") as file:
                contents = file.read()
                print(contents)

            # Get updated values
            new_name = input("Command name (leave empty for same one): ").strip() or command_name
            parts = contents.split()
            new_shebang = input("Shebang (leave empty for same one): ").strip() or parts[0]
            new_interpreter = input("Interpreter (leave empty for same one): ").strip() or parts[1]
            new_source = input("Source (leave empty for same one): ").strip() or parts[2]

            # Create new command
            baked_command = self.bake_command(new_source, new_shebang, new_interpreter)
            self.create_command(new_name, baked_command)

            # Delete old if name changed
            if new_name != command_name:
                self.delete_command(command_name)

        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to edit command: {e}")

    def command_exists(self, command_name: str) -> bool:
        """
        Check if a command exists.
        :param command_name: The command's name to check.
        :return: True or False depending on if the command exists.
        """
        return os.path.exists(self.get_command_path(command_name))

    def view_command(self, command_name: str) -> None:
        """
        View contents of a command.
        :param command_name: The command to be viewed.
        :return: None
        """
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(self.get_command_path(command_name), "r") as file:
                content = file.read().splitlines()
                shebang = content[0]
                command = content[1].split()
                interpreter = command[0]
                path = command[1]
                symbol = command[2]
                # Set a fixed width for the formatted messages
                field_width = 25  #
                print(f"{format_msg(MessageType.SHEBANG):<{field_width}} {shebang}")
                print(f"{format_msg(MessageType.INTERPRETER):<{field_width}} {interpreter}")
                print(f"{format_msg(MessageType.PATH):<{field_width}} {path}")
                print(f"{format_msg(MessageType.SYMBOL):<{field_width}} {symbol}")
        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to read command: {e}")

    def list_commands(self) -> None:
        """
        List all baked commands.
        :return: None
        """
        try:
            # List files, excluding hidden files
            commands = [cmd for cmd in os.listdir(self.commands_path) if not cmd.startswith(".")]

            # Define column widths for consistent formatting
            command_width = 15
            path_width = max(len(os.path.join(self.commands_path, cmd)) for cmd in commands)

            for command in commands:
                full_path = os.path.join(self.commands_path, command)
                # If verbose, include the full path and modification time
                if self.verbose:
                    mod_time = time.ctime(os.path.getmtime(full_path))
                    extra = f" | {full_path:<{path_width}} | {mod_time}"
                else:
                    extra = ""

                # Print command with consistent column widths
                print(f"{format_msg(MessageType.CMD)} {command:<{command_width}} {extra}")

        except OSError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to list commands: {e}")

    def delete_command(self, command_name: str) -> None:
        """
        Delete a command.
        :param command_name: The command to delete.
        :return: None
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
        Get full path for a command.
        :param command_name: The command to get the full path of.
        :return: Path of the inputted command.
        """
        return os.path.join(self.commands_path, command_name)

    def get_command_source(self, command_name: str) -> str | None:
        """
        Gets the command source file path.
        :param command_name: The command's name to get.
        :return: The path of the command's source. *(None if the command doesn't exist)*
        """
        if not self.command_exists(command_name):
            return None

        path = self.get_command_path(command_name)
        with open(path, "r") as file:
            source = file.read().split()[2]
            return source

    @staticmethod
    def bake_command(source: str, shebang: str | None = None, interpreter: str | None = None) -> str:
        """
        Create the command string.
        :param source: The source of the python file.
        :param shebang: The shebang on top of the file.
        :param interpreter: The interpreter to use.
        :return: Compiled string of the baked command.
        """
        shebang = shebang if shebang else "#!" + get_current_shell_path()
        interpreter = interpreter if interpreter else "python3"
        return f"{shebang}\n{interpreter} {source} $@"
