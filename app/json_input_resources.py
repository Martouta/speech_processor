import json


def json_input_resources(filepath):
    '''
    It assumes correct file format and reading permissions.
    It fetches and returns the JSON input containing resources.
    '''
    with open(filepath, 'r') as file:
        text = file.read()
        return json.loads(text)
