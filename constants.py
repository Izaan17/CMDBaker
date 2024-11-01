import getpass
import requests
import os

from utils.console import format_msg, MessageType


def get_latest_version() -> float:
    version_number = -1
    try:
        version = requests.get('https://raw.githubusercontent.com/Izaan17/CMDBaker/refs/heads/master/version.txt')
        version_number = float(version.text)
    except requests.exceptions.RequestException as request_error:
        print(format_msg(MessageType.ERROR), f"Failed to get latest version: {request_error}")
    except Exception as error:
        print(format_msg(MessageType.ERROR), f"An unknown error occurred: {error}")

    return version_number

USER = getpass.getuser()
HOME_PATH = os.path.expanduser('~')
FOLDER_LOCATION = os.path.join(HOME_PATH, 'CMDBaker')
CONFIG_LOCATION = os.path.join(FOLDER_LOCATION, 'config.json')
VERSION = get_latest_version()