import os
from typing import Optional
from utils.console import MessageType, format_msg
from utils.shell import chmod_executable

class CommandHandler:
    def __init__(self, commands_path: str):
        self.commands_path = commands_path

    def create_command(self, command_name: str, baked_command: str, starting_location: Optional[str] = None) -> None:
        """Create a new baked command."""
        location = starting_location or self.commands_path
        full_path = os.path.join(location, command_name)

        try:
            with open(full_path, 'w') as command_file:
                command_file.write(baked_command)
            chmod_executable(full_path)
        except IOError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to create command: {e}")

    def edit_command(self, command_name: str) -> None:
        """Edit an existing command."""
        full_path = self.get_command_path(command_name)
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(full_path, 'r') as file:
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
        """Check if a command exists."""
        return os.path.exists(self.get_command_path(command_name))

    def view_command(self, command_name: str) -> None:
        """View contents of a command."""
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            with open(self.get_command_path(command_name), 'r') as file:
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
        """List all baked commands."""
        try:
            commands = [cmd for cmd in os.listdir(self.commands_path)
                        if cmd != ".DS_Store"]
            for command in commands:
                print(f"{format_msg(MessageType.CMD)} {command}")
        except OSError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to list commands: {e}")

    def delete_command(self, command_name: str) -> None:
        """Delete a command."""
        if not self.command_exists(command_name):
            print(f"{format_msg(MessageType.ERROR)} Command '{command_name}' does not exist")
            return

        try:
            os.remove(self.get_command_path(command_name))
        except OSError as e:
            print(f"{format_msg(MessageType.ERROR)} Failed to delete command: {e}")

    def get_command_path(self, command_name: str) -> str:
        """Get full path for a command."""
        return os.path.join(self.commands_path, command_name)

    @staticmethod
    def bake_command(source: str, shebang: str = "#!/bin/zsh", interpreter: str = "python3") -> str:
        """Create the command string."""
        return f"{shebang}\n{interpreter} {source} $@"

