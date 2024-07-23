from os import path

def flattenDict(_dict, res=None):
    if res is None:
        res = []

    for key, value in _dict.items():
        res.append(key)
        if isinstance(value, dict):
            flattenDict(value, res)
    return res

def file_exists(file_dir):
    return path.exists(file_dir)
