import getpass
import requests
import os

from utils.console import format_msg, MessageType


def get_latest_version() -> float:
    """
    Gets the latest version from the GitHub version file.
    :return: Latest version of CMDBaker. (-1 = Failed to get latest version)
    """
    version_number = -1
    try:
        version = requests.get("https://raw.githubusercontent.com/Izaan17/CMDBaker/refs/heads/master/version.txt")
        version_number = float(version.text)
    except requests.exceptions.RequestException:
        pass
    except Exception as error:
        print(format_msg(MessageType.ERROR), f"An unknown error occurred getting the latest version: {error}")
        pass

    return version_number

USER = getpass.getuser()
HOME_PATH = os.path.expanduser("~")
FOLDER_LOCATION = os.path.join(HOME_PATH, "CMDBaker")
CONFIG_LOCATION = os.path.join(FOLDER_LOCATION, "config.json")