document.addEventListener("DOMContentLoaded", function () {
    const tags = [];

    // Sort the tags array in alphabetical order
    tags.sort();

    const tagSelect = document.getElementById("tagSelect");

    tags.forEach(tag => {
        const tagElement = document.createElement("span");
        tagElement.classList.add("tag");
        tagElement.textContent = tag;
        tagElement.addEventListener("click", () => {
            tagElement.classList.toggle("selected");
            filterAndSearchCards();
        });
        tagSelect.appendChild(tagElement);
    });

    populateTypeFilter();
    filterAndSearchCards();
});

document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll('.search-field');
    textareas.forEach(textarea => {
        textarea.style.height = textarea.scrollHeight + 'px';
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});

function populateTypeFilter() {
    const typeFilter = document.getElementById("typeFilter");
    const types = new Set();

    document.querySelectorAll(".card").forEach(card => {
        const type = card.dataset.type; // Assuming each card has a data-type attribute
        if (type) {
            types.add(type);
        }
    });

    Array.from(types).sort().forEach(type => {
        const option = document.createElement("option");
        option.value = type;
        option.textContent = type;
        typeFilter.appendChild(option);
    });
}

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

function toggleReferences(button) {
    const references = button.nextElementSibling;
    if (references.style.display === "none" || references.style.display === "") {
        references.style.display = "block";
    } else {
        references.style.display = "none";
    }
}

function filterAndSearchCards() {
    const selectedTags = Array.from(document.querySelectorAll(".tag.selected")).map(tag => tag.textContent);
    const input = document.getElementById("searchInput").value.toLowerCase();
    const typeFilterValue = document.getElementById("typeFilter").value;
    const cards = document.querySelectorAll(".card");
    const availableTags = new Set();

    cards.forEach(card => {
        const cardTags = card.dataset.tags.split(" ");
        const matchesTags = selectedTags.length === 0 || selectedTags.every(tag => cardTags.includes(tag));
        const cardName = card.querySelector(".card-header h2").textContent.toLowerCase();
        const searchField = card.querySelector(".search-field");
        const matchesSearch = !input || cardName.includes(input) || searchField.textContent.toLowerCase().includes(input);
        const matchesType = typeFilterValue === "All" || card.dataset.type === typeFilterValue;

        if (matchesTags && matchesSearch && matchesType) {
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
    filterAndSearchCards();
}
