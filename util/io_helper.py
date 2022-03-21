import json


def write_to_file(content, file_name):
    json_str = json.loads(content)
    with open(file_name + ".json", 'w') as f:
        f.write(json.dumps(json_str, indent=2))
        f.close()


def read_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()