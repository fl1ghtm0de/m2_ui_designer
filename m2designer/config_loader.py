import json
from pathlib import Path

class Config:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, cfg_file="config.json"):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.home_dir = Path(__file__).resolve().parent
            with open(cfg_file, 'r') as f:
                config = json.load(f)
                for key, value in config.items():
                    try:
                        attr_value = Path(self.home_dir, value) # if attr is not a path, set it as is
                    except TypeError:
                        attr_value = value

                    setattr(self, key, attr_value)

    def construct_path(self, *args):
        _path = Path()
        for arg in args:
            _path = Path(_path, arg)
        return _path