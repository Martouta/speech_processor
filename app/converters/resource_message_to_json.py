import json

def resource_message_to_json(msg) -> dict:
    resource_message = msg if (type(msg) is dict) else json.loads(msg.value)
    return resource_message['resource'] if ('resource' in resource_message) else resource_message
