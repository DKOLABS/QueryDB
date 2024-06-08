import os
import yaml
from pathlib import Path
from datetime import datetime


def load_yaml_files(directory):
    cards = []
    for item in Path.rglob("*"):
        if item.endswith(".yaml") and item.is_file():
            with open(item, "r") as file:
                card = yaml.safe_load(file)
                cards.append(card)
    return cards


def generate_html(cards):
    header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure Audit Logs</title>
    <style>
/* CSS styles */
body { margin: 0; font-family: 'Roboto', sans-serif; background-color: #f5f5f5; }
.header { background-color: #1c436d; color: white; padding: 20px; text-align: left; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
.header h1 { margin: 0; font-size: 24px; }
.container { display: flex; height: calc(100vh - 60px); }
.sidebar { width: 20%; background-color: #fff; padding: 20px; border-right: 1px solid #ccc; box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); overflow-y: auto; }
.filter { margin-bottom: 20px; }
.filter label { display: block; margin-bottom: 10px; font-weight: bold; color: #333; font-size: 16px; }
.filter input[type="text"] { width: calc(100% - 20px); padding: 10px; border-radius: 5px; border: 1px solid #ccc; box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1); font-size: 14px; }
.tag-select { display: flex; flex-wrap: wrap; gap: 10px; }
.tag-select .tag { display: inline-block; padding: 5px 10px; margin-right: 5px; border-radius: 20px; font-size: 12px; font-weight: bold; cursor: pointer; background-color: #ddd; transition: background-color 0.3s ease; }
.tag-select .tag.selected { background-color: #007bff; color: #fff; }
.content { width: 80%; padding: 20px; overflow-y: auto; }
.card { background: #fff; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); border: 1px solid #e0e0e0; margin-bottom: 20px; overflow: hidden; transition: box-shadow 0.3s ease, transform 0.3s ease; }
.card:hover { box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2); transform: translateY(-5px); }
.card-header { background: #f1f1f1; padding: 20px; border-bottom: 1px solid #ddd; }
.card-header h2 { margin: 0; font-size: 18px; color: #333; }
.card-body { padding: 20px; }
.card-footer { background: #f1f1f1; padding: 20px; border-top: 1px solid #ddd; }
.meta { display: flex; flex-wrap: wrap; margin-bottom: 10px; }
.meta-item { margin-right: 20px; font-size: 14px; line-height: 1.5; }
.meta-title { font-weight: bold; color: #333; }
.meta-value { color: #555; }
.card .tags { margin-top: 10px; }
.card .tag { display: inline-block; padding: 5px 10px; margin-right: 5px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.card .tag.azure { background-color: #007bff; color: #fff; }
.card .tag.windows { background-color: #28a745; color: #fff; }
.card .tag.zscaler { background-color: #55418b; color: #fff; }
.card .tag.ad_win { background-color: #387e6f; color: #fff; }
.search-container { position: relative; margin-top: 10px; }
.search-field { width: 99%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; }
.copy-btn { position: absolute; top: 10px; right: 10px; background-color: #007bff; color: #fff; border: none; border-radius: 4px; padding: 5px 10px; cursor: pointer; }
.copy-btn:active { background-color: #0056b3; }
.copy-btn.clicked { background-color: #28a745; color: white; }
    </style>
</head>
<body>
    <header class="header">
        <h1>Splunk Catalog</h1>
    </header>
    <main class="container">
        <aside class="sidebar">
            <div class="filter">
                <label for="searchInput">Search:</label>
                <input type="text" id="searchInput" onkeyup="searchCards()" placeholder="Search..." aria-label="Search input">
            </div>
            <div class="tag-filter filter">
                <label>Filter by Tags:</label>
                <div id="tagSelect" class="tag-select">
                    <!-- Tags will be dynamically inserted here -->
                </div>
            </div>
        </aside>
        <section class="content" id="content">
       """

    footer = """
        </section>
    </main>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const tags = ["azure", "windows", "zscaler", "ad_win", "security", "network", "cloud", "devops", "monitoring", "compliance"];

            // Sort the tags array in alphabetical order
            tags.sort();

            const tagSelect = document.getElementById("tagSelect");

            tags.forEach(tag => {
                const tagElement = document.createElement("span");
                tagElement.classList.add("tag");
                tagElement.textContent = tag;
                tagElement.addEventListener("click", () => {
                    tagElement.classList.toggle("selected");
                    filterCards();
                });
                tagSelect.appendChild(tagElement);
            });

            filterCards();
        });


        function copyContent(event) {
            const button = event.target;
            const textarea = button.previousElementSibling;
            textarea.select();
            document.execCommand('copy');

            button.classList.add('clicked');
            setTimeout(() => {
                button.classList.remove('clicked');
            }, 2000); // Remove the class after 2 seconds
        }

        function filterCards() {
            const selectedTags = Array.from(document.querySelectorAll(".tag.selected")).map(tag => tag.textContent);
            const cards = document.querySelectorAll(".card");

            cards.forEach(card => {
                const cardTags = card.dataset.tags.split(" ");
                if (selectedTags.length === 0 || selectedTags.every(tag => cardTags.includes(tag))) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        }

        function searchCards() {
            const input = document.getElementById("searchInput").value.toLowerCase();
            const searchFields = document.querySelectorAll(".search-field");

            searchFields.forEach(field => {
                const text = field.textContent.toLowerCase();
                const card = field.closest('.card');
                if (card) {
                    if (text.includes(input)) {
                        card.style.display = "block";
                    } else {
                        card.style.display = "none";
                    }
                }
            });
        }
    </script>
</body>
</html>
       """

    card_template = """
       <article class="card" data-tags="{tags}">
           <header class="card-header">
               <h2>{name}</h2>
               <div class="tags">
                   {tags_html}
               </div>
           </header>
           <div class="card-body">
               <p><strong>Description:</strong> {description}</p>
               <div class="search-container">
                   <textarea class="search-field" readonly rows="8">{search}</textarea>
                   <button class="copy-btn" onclick="copyContent(event)">Copy</button>
               </div>
           </div>
           <footer class="card-footer">
               <div class="meta">
                   <div class="meta-item">
                       <span class="meta-title">Author:</span>
                       <span class="meta-value">{author}</span>
                   </div>
                   <div class="meta-item">
                       <span class="meta-title">Last Updated:</span>
                       <span class="meta-value">{last_updated}</span>
                   </div>
                   <div class="meta-item">
                       <span class="meta-title">Version:</span>
                       <span class="meta-value">{version}</span>
                   </div>
               </div>
           </footer>
       </article>
    """

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
    input_directory = "../searches/"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile_str = Path(f"../build/index_{timestamp}.html")
    cards = load_yaml_files(input_directory)
    html_content = generate_html(cards)

    with open(outfile_str, "w") as file:
        file.write(html_content)


if __name__ == "__main__":
    main()
