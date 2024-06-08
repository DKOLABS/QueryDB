document.addEventListener("DOMContentLoaded", function () {
    const tags = []; // Placeholder, will be replaced by Python script

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
    const availableTags = new Set();

    cards.forEach(card => {
        const cardTags = card.dataset.tags.split(" ");
        const isCardVisible = selectedTags.length === 0 || selectedTags.every(tag => cardTags.includes(tag));

        if (isCardVisible) {
            card.style.display = "block";
            cardTags.forEach(tag => availableTags.add(tag));
        } else {
            card.style.display = "none";
        }
    });

    updateAvailableTags(availableTags, selectedTags);
}

function updateAvailableTags(availableTags, selectedTags) {
    const tagElements = document.querySelectorAll(".tag-select .tag");
    tagElements.forEach(tagElement => {
        const tag = tagElement.textContent;
        if (availableTags.has(tag) || selectedTags.includes(tag)) {
            tagElement.style.display = "inline-block";
        } else {
            tagElement.style.display = "none";
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
