import json

def read_json_file(file_path):
    """
    Reads and parses a JSON file.

    :param file_path: Path to the JSON file
    :return: Parsed JSON data
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data