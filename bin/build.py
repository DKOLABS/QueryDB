import json
import random
import re
from pathlib import Path

import jinja2
import yaml
from bs4 import BeautifulSoup as bs
from bs4 import formatter

ROOT_DIR = Path(__file__).parent.parent


def css_slug(label):
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(label)).strip("_")
    return s or "item"


# Function to generate a random hex color
def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


# Function to calculate the luminance of a hex color
def calculate_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


# Function to determine if a color is readable on a black background
def is_readable_on_black(hex_color):
    luminance = calculate_luminance(hex_color)
    return luminance > 150  # Adjust this threshold as needed


# Function to generate a random color that is readable on a black background
def generate_readable_color():
    while True:
        color = generate_random_color()
        if is_readable_on_black(color):
            return color


# Function to load YAML files from a directory, extracting relevant data
def load_yaml_files(yaml_folder):
    cards = []
    tags = set()
    indexes = set()
    seen_names = {}

    yaml_paths = sorted(yaml_folder.rglob("*.yaml"))

    for yaml_path in yaml_paths:
        print(yaml_path.name)
        with open(yaml_path, "r", encoding="utf-8") as fp:
            card = yaml.safe_load(fp)

        name = card.get("name")
        if not name:
            raise ValueError(f"Missing 'name' in {yaml_path}")
        if name in seen_names:
            raise ValueError(
                f"Duplicate card name {name!r}: {seen_names[name]} and {yaml_path}"
            )
        seen_names[name] = yaml_path

        card["source"] = yaml_path.name
        card["type"] = str(yaml_path.parent.relative_to(yaml_folder))

        if "indexes" not in card or card["indexes"] is None:
            card["indexes"] = []
        if "tags" not in card or card["tags"] is None:
            card["tags"] = []

        card["tag_items"] = [{"label": t, "slug": css_slug(t)} for t in card["tags"]]
        card["index_items"] = [{"label": i, "slug": css_slug(i)} for i in card["indexes"]]

        cards.append(card)
        tags.update(card["tags"])
        indexes.update(card["indexes"])

    return cards, tags, indexes


# Function to render a Jinja2 template with the given context
def render_template(template_path, context):
    template_loader = jinja2.FileSystemLoader(searchpath=template_path.parent)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_path.name)
    return template.render(context)


if __name__ == "__main__":

    # Paths to YAML files and build folder
    build_file = ROOT_DIR / "build" / "output.html"
    yaml_files = ROOT_DIR / "searches"

    # Paths to Jinja2 templates
    header_template = ROOT_DIR / "templates" / "header.html"
    footer_template = ROOT_DIR / "templates" / "footer.html"
    card_template = ROOT_DIR / "templates" / "card.html"
    script_template = ROOT_DIR / "templates" / "script.js"
    style_template = ROOT_DIR / "templates" / "style.css"

    ##########################
    ##### Generate Cards #####
    ##########################

    # Load cards, tags, and indexes from YAML files
    cards, tags, indexes = load_yaml_files(yaml_files)

    # Generate a readable color for each tag and index
    tag_colors = {tag: generate_readable_color() for tag in tags}
    index_colors = {index: generate_readable_color() for index in indexes}

    # Generate HTML for each card (deterministic order: sorted YAML paths)
    cards_html = str()
    for card_data in cards:
        cards_html += render_template(card_template, card_data)

    ###########################
    ##### Generate Header #####
    ###########################

    # Load CSS styles from file
    with open(style_template, "r", encoding="utf-8") as fp:
        css_styles = fp.read()

    # Add tag styles to CSS
    for tag, color in tag_colors.items():
        slug = css_slug(tag)
        css_styles += (
            f"\n.card .tag.{slug} {{ background-color: {color}; color: #000000; }}\n"
        )

    # Add index styles to CSS
    for index, color in index_colors.items():
        slug = css_slug(index)
        css_styles += (
            f".card .index.{slug} {{ background-color: {color}; color: #000000; }}\n"
        )

    css_styles = {"style": css_styles}
    header_html = render_template(header_template, css_styles)

    ###########################
    ##### Generate Footer #####
    ###########################

    # Load JavaScript from file
    with open(script_template, "r", encoding="utf-8") as fp:
        scripts = fp.read()

    # Add tags to JavaScript (JSON for safe embedding)
    tags_js = "const tags = " + json.dumps(sorted(tags)) + ";"
    scripts = scripts.replace("const tags = [];", tags_js)

    # Add indexes to JavaScript
    indexes_js = "const indexes = " + json.dumps(sorted(indexes)) + ";"
    scripts = scripts.replace("const indexes = [];", indexes_js)

    scripts = {"scripts": scripts}
    footer_html = render_template(footer_template, scripts)

    #######################
    ##### Create File #####
    #######################

    # Combine header, cards, and footer into a single HTML file
    html = header_html + cards_html + footer_html

    # Write output file
    if build_file.parent.is_dir() is False:
        build_file.parent.mkdir(parents=True)

    formatter = formatter.HTMLFormatter(indent=4)
    with open(build_file, "w", encoding="utf-8") as out_file:
        out_file.write(bs(html, "html.parser").prettify(formatter=formatter))
