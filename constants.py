import getpass
import os
import requests

from utils.console import format_msg, MessageType

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Izaan17/CMDBaker/refs/heads/master/version.txt"

def fetch_latest_version() -> float:
    """
    Fetches the latest version of CMDBaker from a GitHub URL.

    :return: Latest version of CMDBaker as a float. Returns -1 if an error occurs.
    """
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        return float(response.text.strip())  # Ensure we get the version as a float after stripping whitespace
    except requests.exceptions.RequestException as e:
        print(format_msg(MessageType.ERROR), f"Error fetching version from GitHub: {e}")
    except ValueError as e:
        print(format_msg(MessageType.ERROR), f"Error parsing version: {e}")
    except Exception as e:
        print(format_msg(MessageType.ERROR), f"An unexpected error occurred: {e}")
    return -1

# Path configurations
USER = getpass.getuser()
HOME_PATH = os.path.expanduser("~")
FOLDER_LOCATION = os.path.join(HOME_PATH, "CMDBaker")
CONFIG_LOCATION = os.path.join(FOLDER_LOCATION, "config.json")