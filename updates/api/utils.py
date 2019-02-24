import json

def is_json(raw_data):
    try:
        data = json.loads(raw_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid
