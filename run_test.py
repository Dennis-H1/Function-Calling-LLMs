# This file runs the test and writes the results into a output.json
# To run a test, please specify all the necessary details & arguments in the **test_config.json**.

import os
import json
import argparse

QUESTIONS_FILE_PATH = os.getcwd() + "\questions.json"

print(QUESTIONS_FILE_PATH)


def extract_config():
    pass


def run_test():
    pass


if __name__ == "__main__":

    def _valid_file(path):
        base, ext = os.path.splitext(path)
        if not os.path.isfile(path) or ext.lower() != '.json':
            raise argparse.ArgumentTypeError(
                'File must have a .json extension')
        return path

    parser = argparse.ArgumentParser(
        description='Process the test_config.json file')
    parser.add_argument(
        '--file_path', help='File path to the JSON file', type=_valid_file)
    args = parser.parse_args()

    with open(args.file_path, mode="r") as f:
        config = json.load(f)

    try:
        _valid_file(config["output_file"])

        with open(config["output_file"], mode="r") as f:
            output = json.load(f)

        new_run = {
            "metadata": {
                "id": config["id"],
                "name": config["name"],
                "model": config["model"],
                ""
            },
            "statistics": {},
            "results": {}
        }

        output["runs"].append(new_run)

    except argparse.ArgumentTypeError:
        print("Output file is not a json")
        exit(1)
