import jinja2
import yaml
import random
from pathlib import Path


## Tag Color Functions


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def calculate_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def is_readable_on_black(hex_color):
    luminance = calculate_luminance(hex_color)
    return luminance > 150  # Adjust this threshold as needed


def generate_readable_color():
    while True:
        color = generate_random_color()
        if is_readable_on_black(color):
            return color


## HTML Generator Functions


def load_yaml_file(filepath):
    with open(filepath, "r") as file:
        card = yaml.safe_load(file)
        card["source"] = "/".join(filepath.parts[1:])
        card["search_rows"] = card["search"].count("\n") + 1
        card["tags_string"] = " ".join(card["tags"])
    return card


def write_temp_card(card_data, j2_card_template):
    temp_dir = Path("./build/temp/")
    out_file = Path(temp_dir, card_data["id"] + ".html")
    with open(out_file, "w") as out_file:
        out_file.write(j2_card_template.render(card_data))


def generate_html():
    pass
    ## Build Header

    ## Add Cards

    ## Build Footer

    ## Return/Write HTML


if __name__ == "__main__":
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("build"), trim_blocks=True, lstrip_blocks=True
    )

    j2_card_template = env.get_template("card_jin.html")
    j2_header_template = env.get_template("header_jin.html")
    j2_footer_template = env.get_template("footer_jin.html")
    data_directory = Path("./data/")
    card_index = dict()
    tags = set()

    for file in data_directory.rglob("*.yaml"):
        card_data = load_yaml_file(file)
        card_index[card_data["name"]] = card_data["id"]
        tags.update(card_data["tags"])
        write_temp_card(card_data, j2_card_template)

    tag_colors = {tag: generate_readable_color() for tag in tags}

    ## Header and Style
    with open("./bin/templates/style.css", "r") as file:
        styles = file.read()

    css_styles = styles
    for tag, color in tag_colors.items():
        css_styles += (
            f".card .tag.{tag} {{ background-color: {color}; color: #000000; }}\n"
        )

    style = {"style": css_styles}
    header = j2_header_template.render(style)

    ## Footer
    with open("./bin/templates/scripts.js", "r") as file:
        scripts = file.read()
    tags_js = f"const tags = {sorted(tags)};"
    scripts = scripts.replace("const tags = [];", tags_js)
    scripts = {"scripts": scripts}
    
    footer = j2_footer_template.render(scripts)
    
    card_names = sorted(card_index.keys())

    cards_html = str()

    for card in card_names:
        with open(Path("./build/temp", card_index[card] + ".html"), "r") as file:
            card_html = file.read()
        cards_html += f"{card_html}\n"
    
    html = header + cards_html + footer
    with open(Path("./build/out.html"), "w") as out_file:
        out_file.write(html)
    print(html)