import getpass
import os
import json


class Config:
    def __init__(self, path, data: dict = None):
        self.path = path
        self.data = {}
        if data:
            self.data = data

    def load_config(self):
        with open(self.path, 'r') as config_file:
            self.data = json.loads(config_file.read())
            return self.data

    def get_config(self):
        return self.data

    def write_config(self, data: dict = None):
        """
        Writes config from memory or if passed in to a file path specified.
        :param data: If data is passed in it will overwrite what's in memory.
        """
        d = self.data
        if data:
            d = data
        with open(self.path, 'w') as config_file:
            config_file.write(json.dumps(d))
        self.data = d

    def append_config(self, key, value):
        self.data[key] = value
        self.write_config()


def get_path(prompt, exists=False, create=False):
    while True:
        path = input(prompt)
        if exists:
            if not os.path.exists(path):
                print("[-] Path does not exist please enter a valid path.")
                continue
            else:
                return path
        if create:
            try:
                os.mkdir(path)
            except Exception as error:
                print(error)
                continue
        return path


user = getpass.getuser()
home = os.path.expanduser('~')
folder_location = f"{home}/CMDBaker/"
config_location = f"{folder_location}config.json"
if not os.path.exists(folder_location):
    os.mkdir(folder_location)
config_data = {"main_folder": ""}
if not os.path.exists(config_location):
    print(f""" ____ ____ ____ _________ ____ ____ ____ ____ ____ 
||C |||M |||D |||       |||B |||a |||k |||e |||r ||
||__|||__|||__|||_______|||__|||__|||__|||__|||__||
|/__\\|/__\\|/__\\|/_______\\|/__\\|/__\\|/__\\|/__\\|/__\\|
\t\t\t\tCMD Baker Setup""")
    main_path = get_path("Main Path (all of your scripts will be stored here): ", exists=True, create=True)
    print(f"[+] Created path: {os.path.abspath(main_path)}")
    # Save main path to config
    config_data = {"main_path": main_path, "is_baked": False}
    print(config_location)
    config = Config(config_location)
    config.write_config(config_data)
