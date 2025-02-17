import jinja2
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent


# Function to render a Jinja2 template with the given context
def render_template(template_path, context):
    template_loader = jinja2.FileSystemLoader(searchpath=template_path.parent)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_path.name)
    return template.render(context)


def parse_tags(content):
    # Define regex patterns
    datamodel_pattern = r"datamodel\s*=\s*(\w+)"
    index_pattern = r'(^|\s+)index\s*=\s*"?(\w+)"?|(^|\s+)index\s*IN\s*\(([^)]+)\)'

    # Extract datamodels
    datamodels = re.findall(datamodel_pattern, content)

    # Extract indexes
    indexes = []
    index_matches = re.findall(index_pattern, content)
    for match in index_matches:
        if match[0]:  # Single index
            indexes.append(match[0])
        if match[1]:  # Multiple indexes
            indexes.extend(match[1].replace('"', "").split(","))

    # Clean up indexes list
    indexes = [index.strip() for index in indexes]

    tags = list(set(datamodels) | set(indexes))

    tags = [tag for tag in tags if tag]

    if len(tags) == 0:
        tags.append("None")

    return tags
    

def normalize_json(input_data):
    output_data = dict()

    # API Data
    if "content" in input_data:
        output_data["title"] = input_data["name"]
        output_data["id"] = input_data["id"]
        output_data["author"] = input_data["author"]
        output_data["updated"] = input_data["updated"]
        output_data["disabled"] = input_data["content"]["disabled"]
        output_data["app"] = input_data["acl"]["app"]
        output_data["type"] = (
            "report" if input_data["content"]["alert_type"] == "always" else "alert"
        )
        output_data["description"] = input_data["content"]["description"]
        output_data["search"] = input_data["content"]["search"].replace("\n", "\n  ")
        output_data["cron_schedule"] = input_data["content"]["cron_schedule"]
        output_data["earliest_time"] = input_data["content"]["dispatch.earliest_time"]
        output_data["latest_time"] = input_data["content"]["dispatch.latest_time"]
        output_data["tags"] = parse_tags(input_data["content"]["search"])
    # Manual Data
    else:
        output_data["title"] = input_data["title"]
        output_data["id"] = input_data["id"]
        output_data["author"] = input_data["author"]
        output_data["updated"] = input_data["updated"]
        output_data["disabled"] = input_data["disabled"]
        output_data["app"] = input_data["eai:acl.app"]
        output_data["type"] = (
            "report" if input_data["alert_type"] == "always" else "alert"
        )
        output_data["description"] = input_data["description"].replace("\n", "\n  ")
        output_data["search"] = input_data["search"].replace("\n", "\n  ")
        output_data["cron_schedule"] = input_data["cron_schedule"]
        output_data["earliest_time"] = input_data["dispatch.earliest_time"]
        output_data["latest_time"] = input_data["dispatch.latest_time"]
        output_data["tags"] = parse_tags(input_data["search"])

    return output_data


if __name__ == "__main__":

    # Paths to Jinja2 templates
    saved_search_template = ROOT_DIR / "templates" / "saved_search.yaml"

    # Working Directories
    json_files = ROOT_DIR / "json_data"
    yaml_files = ROOT_DIR / "yaml_data"

    # Processing
    for file in json_files.iterdir():
        if file.is_file() and file.suffix == ".json":
            with open(file, "r", encoding="utf-8") as f:
                file_data = json.load(f)

            normalized_data = normalize_json(file_data)
            output = render_template(saved_search_template, normalized_data)

            out_dir = yaml_files / normalized_data["app"]
            if not out_dir.exists():
                out_dir.mkdir(parents=True, exist_ok=True)

            out_file = out_dir / f"{file.stem}.yaml"

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(output)
