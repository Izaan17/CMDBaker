import os

from config import Config
from constants import FOLDER_LOCATION, CONFIG_LOCATION, get_latest_version
from utils.console import MessageType, format_msg
from utils.filesystem import get_path

ASCII_LOGO = r"""             _    _       _           
 ___ _____ _| |  | |_ ___| |_ ___ ___ 
|  _|     | . |  | . | .'| '_| -_|  _|
|___|_|_|_|___|  |___|__,|_,_|___|_|  
"""


def ensure_base_directory() -> bool:
    """
    Ensure the base application directory exists.

    :return: True if directory was created or exists, False otherwise.
    """
    try:
        os.makedirs(FOLDER_LOCATION, exist_ok=True)
        return True
    except PermissionError:
        print(f"{format_msg(MessageType.ERROR)} Cannot create base directory.")
        return False


def setup_config() -> bool:
    """
    Initialize configuration file with the main path if it doesn't exist.

    :return: True if config was set up successfully, False otherwise.
    """
    # Check if the config file already exists
    if os.path.exists(CONFIG_LOCATION):
        return True

    print(ASCII_LOGO)

    # Prompt user for main path and ensure it's valid
    main_path = get_path(
        "Main Path (where all your baked commands will be stored): ",
        check_if_exists=True,
        create=True
    )

    print(f"{format_msg(MessageType.NOTICE)} Baked path: {os.path.abspath(main_path)}")

    # Prepare the configuration data
    config_data = {
        "main_path": main_path,
        "is_baked": False,
        "version": get_latest_version()
    }

    # Attempt to write the config file
    try:
        config = Config(CONFIG_LOCATION)
        config.write_config(config_data)
        return True
    except Exception as e:
        print(f"{format_msg(MessageType.ERROR)} Failed to write config: {e}")
        return False


def main() -> None:
    """Run the setup process."""
    if not ensure_base_directory():
        return

    if not setup_config():
        return


if __name__ == "__main__":
    main()
