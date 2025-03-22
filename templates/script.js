document.addEventListener("DOMContentLoaded", function () {
    const tags = [];
    const indexes = [];

    // Sort the tags and indexes arrays in alphabetical order
    tags.sort();
    indexes.sort();

    const tagSelect = document.getElementById("tagSelect");
    const indexSelect = document.getElementById("indexSelect");

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

    indexes.forEach(index => {
        const indexElement = document.createElement("span");
        indexElement.classList.add("index");
        indexElement.textContent = index;
        indexElement.addEventListener("click", () => {
            indexElement.classList.toggle("selected");
            filterAndSearchCards();
        });
        indexSelect.appendChild(indexElement);
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

document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById('collapseExpandButton');
    const cards = document.querySelectorAll('.card');
    let allCollapsed = true;

    cards.forEach(card => {
        const cardBody = card.querySelector('.card-body');
        if (cardBody.style.display !== 'none') {
            allCollapsed = false;
        }
    });

    button.textContent = allCollapsed ? 'Expand All' : 'Collapse All';
});

function populateTypeFilter() {
    const typeFilter = document.getElementById("typeFilter");
    const types = new Set();

    document.querySelectorAll(".card").forEach(card => {
        const type = card.dataset.type;
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
    }, 2000);
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
    const selectedIndexes = Array.from(document.querySelectorAll(".index.selected")).map(index => index.textContent);
    const input = document.getElementById("searchInput").value.toLowerCase();
    const typeFilterValue = document.getElementById("typeFilter").value;
    const cards = document.querySelectorAll(".card");
    const availableTags = new Set();
    const availableIndexes = new Set();

    cards.forEach(card => {
        const cardTags = card.dataset.tags.split(" ");
        const cardIndexes = card.dataset.indexes.split(" ");
        const matchesTags = selectedTags.length === 0 || selectedTags.every(tag => cardTags.includes(tag));
        const matchesIndexes = selectedIndexes.length === 0 || selectedIndexes.every(index => cardIndexes.includes(index));
        const cardName = card.querySelector(".card-header h2").textContent.toLowerCase();
        const searchField = card.querySelector(".search-field");
        const matchesSearch = !input || cardName.includes(input) || searchField.textContent.toLowerCase().includes(input);
        const matchesType = typeFilterValue === "All" || card.dataset.type === typeFilterValue;

        if (matchesTags && matchesIndexes && matchesSearch && matchesType) {
            card.style.display = "block";
            cardTags.forEach(tag => availableTags.add(tag));
            cardIndexes.forEach(index => availableIndexes.add(index));
        } else {
            card.style.display = "none";
        }
    });

    updateAvailableTags(availableTags, selectedTags);
    updateAvailableIndexes(availableIndexes, selectedIndexes);
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

function updateAvailableIndexes(availableIndexes, selectedIndexes) {
    const indexElements = document.querySelectorAll(".index-select .index");
    indexElements.forEach(indexElement => {
        const index = indexElement.textContent;
        if (availableIndexes.has(index) || selectedIndexes.includes(index)) {
            indexElement.style.display = "inline-block";
        } else {
            indexElement.style.display = "none";
        }
    });
}

function searchCards() {
    filterAndSearchCards();
}

function copyCardContentToJson(card) {
    const cardContent = {
        name: card.querySelector(".card-header h2").textContent.trim().replace(/\n/g, ""),
        search: card.querySelector(".search-field").textContent.trim(),
        tags: card.dataset.tags.split(" "),
        indexes: card.dataset.indexes.split(" "),
        type: card.dataset.type
    };

    const jsonString = JSON.stringify(cardContent, null, 2);
    copyToClipboard(jsonString);

    const button = card.querySelector(".copy-json-btn");
    button.classList.add('clicked');
    setTimeout(() => {
        button.classList.remove('clicked');
    }, 2000);
}

function copyToClipboard(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
}

function toggleCollapse(card) {
    const cardBody = card.querySelector('.card-body');
    const cardFooter = card.querySelector('.card-footer');
    const indexes = card.querySelector('.indexes');
    const tags = card.querySelector('.tags');
    const line = card.querySelector('hr.solid');
    const collapseButton = card.querySelector('.collapse-btn');

    if (cardBody.style.display === 'none') {
        cardBody.style.display = 'block';
        cardFooter.style.display = 'block';
        indexes.style.display = 'block';
        tags.style.display = 'block';
        line.style.display = 'block';
        collapseButton.textContent = 'Collapse';
    } else {
        cardBody.style.display = 'none';
        cardFooter.style.display = 'none';
        indexes.style.display = 'none';
        tags.style.display = 'none';
        line.style.display = 'none';
        collapseButton.textContent = 'Expand';
    }
}

function toggleCollapseExpandAll() {
    const cards = document.querySelectorAll('.card');
    const button = document.getElementById('collapseExpandButton');
    const isCollapsed = button.textContent === 'Collapse All';

    cards.forEach(card => {
        const cardBody = card.querySelector('.card-body');
        const cardFooter = card.querySelector('.card-footer');
        const indexes = card.querySelector('.indexes');
        const tags = card.querySelector('.tags');
        const line = card.querySelector('hr.solid');
        const collapseButton = card.querySelector('.collapse-btn');

        if (isCollapsed) {
            cardBody.style.display = 'none';
            cardFooter.style.display = 'none';
            indexes.style.display = 'none';
            tags.style.display = 'none';
            line.style.display = 'none';
            if (collapseButton) collapseButton.textContent = 'Expand';
        } else {
            cardBody.style.display = 'block';
            cardFooter.style.display = 'block';
            indexes.style.display = 'block';
            tags.style.display = 'block';
            line.style.display = 'block';
            if (collapseButton) collapseButton.textContent = 'Collapse';
        }
    });

    button.textContent = isCollapsed ? 'Expand All' : 'Collapse All';
}