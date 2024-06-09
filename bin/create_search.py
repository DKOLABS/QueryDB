import uuid
import yaml
import re
from datetime import datetime
import configparser
from pathlib import Path

CONFIG_FILE = "config.ini"
DATA_DIR = Path("./data/")


def get_user_input(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    return input(prompt) or default


def load_config():
    config = configparser.ConfigParser()
    if Path(CONFIG_FILE).exists():
        config.read(CONFIG_FILE)
    return config


def save_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def list_categories():
    return [d.name for d in DATA_DIR.iterdir() if d.is_dir()]


def get_category():
    categories = list_categories()
    print("Select a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")
    print(f"{len(categories) + 1}. Create a new category")

    try:
        choice = int(get_user_input("Enter the number of your choice: "))
    except ValueError:
        choice = -1

    if 1 <= choice <= len(categories):
        return categories[choice - 1]
    elif choice == len(categories) + 1:
        new_category = get_user_input("Enter the name of the new category: ")
        (DATA_DIR / new_category).mkdir(parents=True, exist_ok=True)
        return new_category
    else:
        print("\nInvalid choice. Please try again.")
        return get_category()


def get_current_names_and_ids():
    data_dir = Path("./data/")
    names = list()
    ids = list()

    for file in data_dir.rglob("*.yaml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f)
        names.append(data["name"])
        ids.append(data["id"])

    return names, ids


def validate_field(field, data_set):
    if field in data_set:
        return False
    else:
        return True


def safe_filename(input_string):
    # Replace spaces with underscores
    safe_name = input_string.replace(" ", "_")
    # Convert to lowercase
    safe_name = safe_name.lower()
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    safe_name = re.sub(r"[^a-z0-9_-]", "", safe_name)
    return safe_name


def main():
    # Load configuration
    config = load_config()

    names, ids = get_current_names_and_ids()

    print("\nNew Search Helper Script\n")

    # Get author from config or prompt the user
    default_author = config.get("DEFAULT", "author", fallback=None)
    author = get_user_input("Enter the author email: ", default=default_author)

    # Collect other user inputs
    while True:
        name = get_user_input("Enter the name: ")
        if validate_field(name, names):
            break
        else:
            print("Name must be unique")

    description = get_user_input("Enter the description: ")
    category = get_category()

    # Auto-generate fields
    while True:
        id = str(uuid.uuid4())
        if validate_field(id, ids):
            break

    last_updated = datetime.now().strftime("%Y-%m-%d")
    version = 1

    # Tags input as a comma-separated string, converted to a list
    tags_input = get_user_input("Enter the tags (comma-separated): ")
    try:
        tags = [tag.strip() for tag in tags_input.split(",")]
    except AttributeError:
        tags = ["none"]

    # Create the data dictionary
    data = {
        "name": name,
        "id": id,
        "author": author,
        "last_updated": last_updated,
        "version": version,
        "description": description,
        "search": "",
        "tags": tags,
    }

    # Write to a YAML file in the specified category directory
    output_file = DATA_DIR / category / str(safe_filename(data["name"]) + ".yaml")
    with open(output_file, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, width=144)

    print(f"YAML file '{output_file}' created successfully.")

    # Update and save the config with the latest author
    config["DEFAULT"] = {"author": author}
    save_config(config)


if __name__ == "__main__":
    main()
