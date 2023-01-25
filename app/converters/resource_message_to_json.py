import json


def resource_message_to_json(msg) -> dict:
    """
    This function converts a message object in a json format to a python dictionary.
    It also checks if the message object is already in a dictionary format and returns it.
    :param msg: message object in json format or dictionary
    :type msg: str or dict
    :return: dictionary representation of the json message
    :rtype: dict
    """
    resource_message = msg if (type(msg) is dict) else json.loads(msg.value)
    return resource_message['resource'] if ('resource' in resource_message) else resource_message
