import json

def read_json(path):
    f = open(path, encoding="utf8")
    data = json.load(f)
    f.close()
    return data