const searchInput = document.querySelector("#ontology-category-search");
const searchResultsElement = document.querySelector("#ontology-category-search-results");
const searchableList = document.querySelector(".list-group-searchable");
const searchableListItemText = Array.from(searchableList.children).reduce(
    (accumulator, currentValue) => {
        accumulator[currentValue.id] = currentValue.textContent.trim();
        return accumulator;
    },
    {}
);
const searchableListClone = searchableList.cloneNode(true);

function updateResourceCount(numResourceCount, reset = false) {
    const resultsCountText = `${numResourceCount} ${(numResourceCount === 1) ? 'category' : 'categories'}`;
    if (reset) {
        return searchResultsElement.textContent = resultsCountText;
    }
    return searchResultsElement.textContent = `Found ${resultsCountText}`;
}

function filterOntologyCategoryList() {
    const searchInputValue = searchInput.value.trim();
    // If search query is blank or just spaces
    if (!searchInputValue) {
        updateResourceCount(searchableListClone.childElementCount, true);
        return searchableList.replaceChildren(...searchableListClone.cloneNode(true).children);
    }
    // Find matches by splitting search query by whitespace
    // and checking if any category names contain all of
    // the parts of the split string.
    const searchInputValueSplit = searchInputValue.split(/\s/);
    const fragment = new DocumentFragment();
    for (const property in searchableListItemText) {
        const listItemText = searchableListItemText[property];
        if (!searchInputValueSplit.every((searchInputValuePart) => listItemText.toLowerCase().includes(searchInputValuePart.toLowerCase()))) {
            continue;
        }
        const listItem = searchableListClone.querySelector(`#${property}`);
        try {
            fragment.append(listItem.cloneNode(true));
        } catch (error) {
            console.error(error);
        }
    }
    updateResourceCount(fragment.childElementCount, true);
    return searchableList.replaceChildren(fragment);
}

searchInput.addEventListener("input", () => {
    filterOntologyCategoryList();
});

window.addEventListener("load", () => {
    filterOntologyCategoryList();
});