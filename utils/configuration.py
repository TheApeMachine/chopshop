import yaml

class Configuration:
    _instance = None

    def __new__(cls):
        print("Initializing configuration")
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        print("Loading configuration")
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default

        return value

config = Configuration()