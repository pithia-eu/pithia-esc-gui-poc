const searchResultsSection = document.querySelector(".section-search-results");
const searchResultsSectionList = searchResultsSection.querySelector("ul");
const dataCollectionCategorySections = document.querySelectorAll(".section-data-collection-list");

const searchInput = document.querySelector("#resource-name-search");
const searchableListItems = document.querySelectorAll(".list-group-searchable li");
const searchableListItemText = Array.from(searchableListItems).reduce((accumulator, currentValue) => {
    accumulator[currentValue.id] = currentValue.textContent.trim();
    return accumulator;
}, {});

const resourceListCount = document.querySelector("#resource-list-count");
const typeReadable = JSON.parse(document.querySelector("#type-readable").textContent);
const typePluralReadable = JSON.parse(document.querySelector("#type-plural-readable").textContent);


function updateResourceCount(numResourceCount, reset = false) {
    const resourceCountText = `${numResourceCount} ${(numResourceCount === 1) ? typeReadable : typePluralReadable}`;
    if (reset) {
        return resourceListCount.textContent = resourceCountText;
    }
    return resourceListCount.textContent = `Found ${resourceCountText}`;
}

export function filterResourceList() {
    const searchInputValue = searchInput.value;
    if (!searchInputValue) {
        updateResourceCount(Object.keys(searchableListItemText).length, typeReadable, typePluralReadable, true);
        searchResultsSection.classList.add("d-none");
        dataCollectionCategorySections.forEach(section => {
            section.classList.remove("d-none");
        });
        return searchResultsSectionList.replaceChildren();
    }
    searchResultsSection.classList.remove("d-none");
    dataCollectionCategorySections.forEach(section => {
        section.classList.add("d-none");
    });
    const fragment = new DocumentFragment();
    for (const property in searchableListItemText) {
        const listItemText = searchableListItemText[property];
        if (!listItemText.toLowerCase().includes(searchInputValue.toLowerCase())) {
            continue;
        }
        try {
            const listItem = document.querySelector(`#${property}`);
            fragment.append(listItem.cloneNode(true));
        } catch (error) {
            console.error(error);
        }
    }
    updateResourceCount(fragment.childElementCount, typeReadable, typePluralReadable);
    return searchResultsSectionList.replaceChildren(fragment);
}

searchInput.addEventListener("input", () => {
    filterResourceList();
});

window.addEventListener("load", () => {
    filterResourceList();
});