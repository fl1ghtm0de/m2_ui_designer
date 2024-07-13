def flattenDict(_dict, res=None):
    if res is None:
        res = []

    for key, value in _dict.items():
        res.append(key)
        if isinstance(value, dict) and len(value.keys()) > 0:
            return flattenDict(value, res)

    return res