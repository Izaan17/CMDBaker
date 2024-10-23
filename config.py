import json


class Config:
    def __init__(self, path, data: dict = None):
        self.path = path
        self.data = data if data else {}

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
