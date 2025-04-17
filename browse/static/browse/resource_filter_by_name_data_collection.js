import {
    disableScrollContainerForSection,
    enableScrollContainerForSection,
} from "/static/browse/data_collection_list.js";


const searchInput = document.querySelector("#resource-name-search");
const resourceListCount = document.querySelector("#resource-list-count");
const typeReadable = JSON.parse(document.querySelector("#type-readable").textContent);
const typePluralReadable = JSON.parse(document.querySelector("#type-plural-readable").textContent);

const dataCollectionTypeSections = Array.from(document.querySelectorAll(".section-data-collection-list"));
const listItemsCategorised = dataCollectionTypeSections.reduce(categoriseDataCollectionListItemsByType, {});
const listItems = document.querySelectorAll(".section-data-collection-list li");

function updateResourceCount(numResourceCount) {
    const resourceCountText = `${numResourceCount} ${(numResourceCount === 1) ? typeReadable : typePluralReadable}`;
    return resourceListCount.textContent = resourceCountText;
}

function categoriseDataCollectionListItemsByType(accumulator, section) {
    const dataCollectionListItemsInSection = Array.from(section.querySelectorAll(".data-collection-list-item"));
    accumulator[section.id] = dataCollectionListItemsInSection;
    return accumulator;
}

function searchDataCollectionListItemsForSection(searchInputValueParts, listItems) {
    let numMatchesFoundInSection = 0;
    listItems.forEach(listItem => {
        const dataCollectionLink = listItem.querySelector("a");
        if (searchInputValueParts.every(part => dataCollectionLink.textContent.toLowerCase().includes(part))) {
            numMatchesFoundInSection += 1
            return listItem.classList.remove("d-none");
        }
        return listItem.classList.add("d-none");
    });
    return numMatchesFoundInSection;
}

function resetSearch() {
    dataCollectionTypeSections.forEach(section => {
        enableScrollContainerForSection(section);
        section.classList.remove("d-none");
    });
    listItems.forEach(listItem => {
        listItem.classList.remove("d-none");
    });
    updateResourceCount(listItems.length);
}

function searchDataCollectionListItems(searchInputValue) {
    const searchInputValueParts = searchInputValue.toLowerCase().split(/\s+/);
    let totalMatchesFound = 0;
    for (const sectionId in listItemsCategorised) {
        const section = document.querySelector(`#${sectionId}`);
        const sectionListItems = listItemsCategorised[sectionId];
        const numMatchesFoundInSection = searchDataCollectionListItemsForSection(
            searchInputValueParts,
            sectionListItems
        );
        if (numMatchesFoundInSection === 0) {
            section.classList.add("d-none");
            continue;
        }
        totalMatchesFound += numMatchesFoundInSection;
        section.classList.remove("d-none");
        disableScrollContainerForSection(section);
    }
    updateResourceCount(totalMatchesFound);
}

searchInput.addEventListener("input", () => {
    const searchInputValue = searchInput.value;
    if (searchInputValue.trim() === "") {
        return resetSearch();
    }
    return searchDataCollectionListItems(searchInputValue);
});

window.addEventListener("load", () => {
    const searchInputValue = searchInput.value;
    if (searchInputValue.trim() !== "") {
        searchDataCollectionListItems(searchInputValue);
    }
});