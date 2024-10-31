import getpass
import os

USER = getpass.getuser()
HOME_PATH = os.path.expanduser('~')
FOLDER_LOCATION = os.path.join(HOME_PATH, 'CMDBaker')
CONFIG_LOCATION = os.path.join(FOLDER_LOCATION, 'config.json')
VERSION = 1.3