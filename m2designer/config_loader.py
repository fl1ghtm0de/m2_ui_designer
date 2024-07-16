import json
from pathlib import Path

class Config:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.home_dir = Path(__file__).resolve().parent
            with open("config.json", 'r') as f:
                config = json.load(f)
                for key, value in config.items():
                    setattr(self, key, Path(self.home_dir, value))

    def construct_path(self, *args):
        _path = Path()
        for arg in args:
            _path = Path(_path, arg)
        return _path