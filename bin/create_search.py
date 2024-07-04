import uuid
import yaml
import re
import inquirer
import os
import subprocess
import tempfile
from datetime import datetime
import configparser
from pathlib import Path

CONFIG_FILE = Path("./bin/config.ini")
DATA_DIR = Path("./data/")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_config():
    config = configparser.ConfigParser(allow_no_value=True)
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE)
    else:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.touch()
    return config


def save_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def get_current_names_and_ids():
    names, ids = [], []

    for file in DATA_DIR.rglob("*.yaml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
        names.append(data["name"])
        ids.append(data["id"])

    return names, ids


def validate_field(field, data_set):
    return field not in data_set


def safe_filename(input_string):
    return re.sub(r"[^a-z0-9_-]", "", input_string.replace(" ", "_").lower())


def get_type(config):
    if not config.has_section("TYPES"):
        config.add_section("TYPES")

    types = list(config._sections["TYPES"].keys())
    types.append("Create new type")
    question = [
        inquirer.List(
            "type",
            message="Select a type",
            choices=types,
        ),
    ]

    answer = inquirer.prompt(question)

    if answer["type"] == "Create new type":
        new_type = inquirer.text(message="Enter new type")
        config["TYPES"][new_type] = None
        save_config(config)
        return new_type
    return answer["type"]


def get_directory_path(base_path=DATA_DIR):
    def list_directories(current_path):
        directories = [d.name for d in current_path.iterdir() if d.is_dir()]
        directories.extend(["Select this folder", "Create new folder"])
        return directories

    current_path = base_path

    while True:
        clear_screen()
        directories = list_directories(current_path)
        questions = [
            inquirer.List(
                "directory",
                message=f"Select a directory under {current_path} or create a new one:",
                choices=directories,
            ),
        ]

        answers = inquirer.prompt(questions)
        selected_directory = answers["directory"]

        if selected_directory == "Create new folder":
            new_folder_name = inquirer.text(
                message="Enter the name of the new folder: "
            )
            new_folder_path = current_path / new_folder_name
            new_folder_path.mkdir(parents=True, exist_ok=True)
            current_path = new_folder_path
        elif selected_directory == "Select this folder":
            break
        else:
            current_path = current_path / selected_directory

    return current_path


def get_multiline_input():
    editor = "notepad" if os.name == "nt" else os.getenv("EDITOR", "gedit")

    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as temp_file:
        temp_file_path = temp_file.name

    subprocess.call([editor, temp_file_path])

    with open(temp_file_path, "r") as temp_file:
        input_text = temp_file.read()

    os.remove(temp_file_path)
    return input_text


def main():
    config = load_config()
    DATA_DIR.mkdir(exist_ok=True)
    names, ids = get_current_names_and_ids()

    print("\nNew Search Helper Script\n")

    questions = [
        inquirer.Text(
            "author",
            message="Enter the author email",
            default=config.get("DEFAULT", "author", fallback=None),
        ),
        inquirer.Text("name", message="Enter the name"),
        inquirer.Text("description", message="Enter the description"),
        inquirer.Text("tags", message="Enter the tags (comma-separated)"),
    ]

    answers = inquirer.prompt(questions)

    while not validate_field(answers["name"], names):
        print("Name must be unique")
        answers["name"] = inquirer.text(message="Enter the name")

    search_type = get_type(config)
    file_dir = get_directory_path()

    while True:
        id = str(uuid.uuid4())
        if validate_field(id, ids):
            break

    last_updated = datetime.now().strftime("%Y-%m-%d")
    version = 1

    tags = (
        [tag.strip() for tag in answers["tags"].split(",")]
        if answers["tags"]
        else ["none"]
    )

    search = get_multiline_input().replace("\n", "\n  ")

    data = {
        "name": answers["name"],
        "id": id,
        "author": answers["author"],
        "last_updated": last_updated,
        "version": version,
        "type": search_type,
        "description": answers["description"],
        "tags": tags,
    }

    output_file = file_dir / f"{safe_filename(data['name'])}.yaml"
    with open(output_file, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, width=144)
        file.write("search: |\n  ")
        file.write(search)

    print(f"YAML file '{output_file}' created successfully.")

    config["DEFAULT"] = {"author": answers["author"]}
    save_config(config)


if __name__ == "__main__":
    main()
