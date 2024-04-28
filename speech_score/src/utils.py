import json
import os


def get_threshold(config_file_path):
    """
    Get the threshold value from the configuration file.
    :return: threshold value
    """
    # Load the configuration file
    config = read_json_file(config_file_path)
    # Get the threshold value from the configuration file
    threshold = config[0]['threshold']
    return threshold


def read_json_file(file_path):
    """
    Reads and parses a JSON file.

    :param file_path: Path to the JSON file
    :return: Parsed JSON data
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json_file(data, file_path="learner_output.json"):
    """
    write a JSON file.

    :param data: data need to be saved as  JSON file
    :param file_path: Specify the file path where you want to save the JSON data
    :return: Parsed JSON data
    """

    # Save the dictionary as a JSON file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


def get_config(config_file_path):
    """
    Get the threshold value from the configuration file.
    :return: threshold value
    """
    # Load the configuration file
    config = read_json_file(config_file_path)

    return config

def get_config_key(key_name="huggingfaceTOKEN"):
    '''

    :param key_name:
    :return:
    '''

    config = get_config("speech_score/data/config/config.json")
    return config[0][key_name]