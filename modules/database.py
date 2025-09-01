import json
import os

current_file_path = os.path.abspath(__file__)  # current file path
modules_dir = os.path.dirname(
    current_file_path
)  # current folder path that database.py is in
base_dir = os.path.dirname(modules_dir)  # current folder path that modules folder is in
data_dir = os.path.join(base_dir, "data")  # current folder path that data folder is in


def load_data(filename):
    file_path = os.path.join(data_dir, filename)

    if not os.path.exists(file_path):
        save_data(filename, [])
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return []


def save_data(filename, data):
    file_path = os.path.join(data_dir, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
