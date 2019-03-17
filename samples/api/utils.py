import json

def is_json(input_data):
    '''
    :returns True if input_data is JSON. else return False
    '''

    try:
        obj = json.loads(input_data)
    except ValueError:
        return False
    return True