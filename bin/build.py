import jinja2
import yaml
import random
from pathlib import Path
from bs4 import BeautifulSoup as bs
from bs4 import formatter

ROOT_DIR = Path(__file__).parent.parent


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
    cards = list()
    tags = set()
    indexes = set()
    card_titles = list()

    for file in yaml_folder.rglob("*.yaml"):
        print(file.name)
        with open(file, "r") as file:
            card = yaml.safe_load(file)
        card["source"] = file.name

        if "indexes" not in card or card["indexes"] is None:
            card["indexes"] = list()
        card["indexes_string"] = " ".join(card["indexes"])

        if "tags" not in card or card["tags"] is None:
            card["tags"] = list()
        card["tags_string"] = " ".join(card["tags"])

        cards.append(card)
        tags.update(card["tags"])
        indexes.update(card["indexes"])
        card_titles.append(card["name"])

    return cards, tags, indexes, sorted(card_titles)


# Function to render a Jinja2 template with the given context
def render_template(template_path, context):
    template_loader = jinja2.FileSystemLoader(searchpath=template_path.parent)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_path.name)
    return template.render(context)


if __name__ == "__main__":

    # Paths to YAML files, temporary and build folder
    build_file = ROOT_DIR / "build" / "output.html"
    yaml_files = ROOT_DIR / "searches"
    temp_folder = ROOT_DIR / "build" / "temp"

    # Paths to Jinja2 templates
    header_template = ROOT_DIR / "templates" / "header.html"
    footer_template = ROOT_DIR / "templates" / "footer.html"
    card_template = ROOT_DIR / "templates" / "card.html"
    script_template = ROOT_DIR / "templates" / "script.js"
    style_template = ROOT_DIR / "templates" / "style.css"

    ##########################
    ##### Generate Cards #####
    ##########################

    # Load cards, tags, and card titles from YAML files
    cards, tags, indexes, card_titles = load_yaml_files(yaml_files)

    # Generate a readable color for each tag and index
    tag_colors = {tag: generate_readable_color() for tag in tags}
    index_colors = {index: generate_readable_color() for index in indexes}

    # Generate HTML for each card
    cards_html = str()
    for card_title in card_titles:
        card_data = [d for d in cards if d.get("name") == card_title][0]
        cards_html += render_template(card_template, card_data)

    ###########################
    ##### Generate Header #####
    ###########################

    # Load CSS styles from file
    with open(style_template, "r") as file:
        css_styles = file.read()

    # Add tag styles to CSS
    for tag, color in tag_colors.items():
        css_styles += (
            f"\n.card .tag.{tag} {{ background-color: {color}; color: #000000; }}\n"
        )

    # Add index styles to CSS
    for index, color in index_colors.items():
        css_styles += (
            f".card .index.{index} {{ background-color: {color}; color: #000000; }}\n"
        )

    css_styles = {"style": css_styles}
    header_html = render_template(header_template, css_styles)

    ###########################
    ##### Generate Footer #####
    ###########################

    # Load JavaScript from file
    with open(script_template, "r") as file:
        scripts = file.read()

    # Add tags to JavaScript
    tags_js = f"const tags = {sorted(tags)};"
    scripts = scripts.replace("const tags = [];", tags_js)

    # Add indexes to JavaScript
    indexes_js = f"const indexes = {sorted(indexes)};"
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