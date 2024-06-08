import yaml
import random
from pathlib import Path
from datetime import datetime


def load_yaml_files(directory):
    cards = []
    for item in directory.rglob("*"):
        if item.is_file():
            with open(item, "r") as file:
                card = yaml.safe_load(file)
                cards.append(card)
    return cards


def read_template_file(filename):
    with open(filename, "r") as file:
        return file.read()


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def generate_html(cards):
    tags = {tag for card in cards for tag in card.get("tags", [])}
    print(type(tags))
    tag_colors = {tag: generate_random_color() for tag in tags}

    styles = read_template_file(Path("templates/style.css"))
    header_template = read_template_file(Path("templates/header.html"))
    footer_template = read_template_file(Path("templates/footer.html"))
    card_template = read_template_file(Path("templates/card.html"))
    scripts = read_template_file(Path("templates/scripts.js"))

    css_styles = styles
    for tag, color in tag_colors.items():
        css_styles += f"""
.card .tag.{tag} {{ background-color: {color}; color: #fff; }}
        """

    tags_js = f"const tags = {list(tags)};"

    scripts = scripts.replace("const tags = [];", tags_js)

    header = header_template.replace(
        '<link rel="stylesheet" href="styles.css">', f"<style>{css_styles}</style>"
    )
    footer = footer_template.replace(
        '<script src="scripts.js"></script>', f"<script>{scripts}</script>"
    )

    cards_html = ""
    for card in cards:
        tags = " ".join(card.get("tags", []))
        tags_html = " ".join(
            [f'<span class="tag {tag}">{tag}</span>' for tag in card.get("tags", [])]
        )
        card_html = card_template.format(
            name=card.get("name"),
            tags=tags,
            tags_html=tags_html,
            description=card.get("description"),
            search=card.get("search"),
            author=card.get("author"),
            last_updated=card.get("last_updated"),
            version=card.get("version"),
        )
        cards_html += card_html

    return header + cards_html + footer


def main():
    input_directory = Path("../searches/")
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamp = "test"
    outfile_str = Path(f"../build/index_{timestamp}.html")
    cards = load_yaml_files(input_directory)
    html_content = generate_html(cards)

    with open(outfile_str, "w") as file:
        file.write(html_content)


if __name__ == "__main__":
    main()
