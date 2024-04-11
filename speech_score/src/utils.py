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