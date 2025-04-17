const searchInput = document.querySelector("#resource-name-search");
const categorySections = Array.from(document.querySelectorAll(".category-section"));
const listItemsCategorised = categorySections.reduce(categoriseEntryListItemsByStaticDataset, {});
// For resetting the search
const listItemsInCategorySections = document.querySelectorAll(".category-section li");
const detailsElementsInCategorySections = document.querySelectorAll(".category-section details");
const hiddenEntryCountElements = document.querySelectorAll(".hidden-entry-count");
const hiddenDataSubsetCountElements = document.querySelectorAll(".hidden-data-subset-count");

const staticDatasetEntryTypeReadable = document.querySelector("#type-readable");
const staticDatasetEntryTypePluralReadable = document.querySelector("#type-plural-readable");


function categoriseDataSubsetListItemsByEntry(accumulator, entryListItem) {
    const dataSubsetListItems = Array.from(entryListItem.querySelectorAll(".data-subset-list-item"));
    accumulator[entryListItem.id] = dataSubsetListItems;
    return accumulator;
}

function categoriseEntryListItemsByStaticDataset(accumulator, staticDatasetSection) {
    const entryListItemsInSection = Array.from(staticDatasetSection.querySelectorAll(".static-dataset-entry-list-item"));
    const dataSubsetListItemsByEntryId = entryListItemsInSection.reduce(categoriseDataSubsetListItemsByEntry, {});
    accumulator[staticDatasetSection.id] = dataSubsetListItemsByEntryId;
    return accumulator;
}

function searchDataSubsetListItems(searchInputParts, entryListItem, dataSubsetListItems) {
    if (!dataSubsetListItems.length) {
        return false;
    }
    let isMatchFoundInDataSubsetListItems = false;
    const hiddenDataSubsetListItems = [];
    for (const listItem of dataSubsetListItems) {
        const dataSubsetLink = listItem.querySelector(".data-subset-link");
        const isMatchFoundInDataSubsetName = searchInputParts.every(part => dataSubsetLink.textContent.toLowerCase().includes(part)) ;
        isMatchFoundInDataSubsetListItems = isMatchFoundInDataSubsetListItems || isMatchFoundInDataSubsetName;
        if (isMatchFoundInDataSubsetName) {
            listItem.classList.remove("d-none");
            continue;
        }
        listItem.classList.add("d-none");
        hiddenDataSubsetListItems.push(listItem);
    }
    const hiddenDataSubsetCount = entryListItem.querySelector(".hidden-data-subset-count");
    hiddenDataSubsetCount.textContent = "";
    if (hiddenDataSubsetListItems.length) {
        hiddenDataSubsetCount.textContent = `(${hiddenDataSubsetListItems.length} hidden)`;
    }
    const entryListItemDetails = entryListItem.querySelector('details');
    if (isMatchFoundInDataSubsetListItems) {
        entryListItemDetails.setAttribute("open", "");
        return isMatchFoundInDataSubsetListItems;
    }
    entryListItemDetails.removeAttribute("open", "");
    return isMatchFoundInDataSubsetListItems;
}

function searchStaticDatasetEntryListItems(searchInputParts, sectionId) {
    let isMatchFoundInSection = false;
    const hiddenEntryListItems = [];
    const section = document.querySelector(`#${sectionId}`);
    const sectionObject = listItemsCategorised[sectionId];
    for (const entryListItemId in sectionObject) {
        let isMatchFoundInEntryListItem = false;
        const entryListItem = section.querySelector(`#${entryListItemId}`);
        const entryLink = entryListItem.querySelector(".static-dataset-entry-link");
        const isMatchFoundInDataSubsetListItems = searchDataSubsetListItems(
            searchInputParts,
            entryListItem,
            sectionObject[entryListItemId]
        );
        isMatchFoundInEntryListItem = searchInputParts.every(part => entryLink.textContent.toLowerCase().includes(part)) || isMatchFoundInDataSubsetListItems;
        isMatchFoundInSection = isMatchFoundInSection || isMatchFoundInEntryListItem;
        if (isMatchFoundInEntryListItem) {
            entryListItem.classList.remove("d-none");
            continue;
        }
        entryListItem.classList.add("d-none");
        hiddenEntryListItems.push(entryListItem);
    }
    const hiddenEntryCount = section.querySelector(".hidden-entry-count");
    if (!hiddenEntryCount) {
        return isMatchFoundInSection;
    }
    hiddenEntryCount.textContent = "";
    if (hiddenEntryListItems.length) {
        hiddenEntryCount.textContent = `(${hiddenEntryListItems.length} hidden)`;
    }
    return isMatchFoundInSection;
}

function resetSearch() {
    categorySections.forEach(section => {
        section.classList.remove("d-none");
    });
    listItemsInCategorySections.forEach(listItem => {
        listItem.classList.remove("d-none");
    });
    hiddenEntryCountElements.forEach(element => {
        element.textContent = "";
    });
    hiddenDataSubsetCountElements.forEach(element => {
        element.textContent = "";
    });
    detailsElementsInCategorySections.forEach(element => {
        element.removeAttribute("open");
    });
}

function searchCategorySection(searchInputValue) {
    const searchInputParts = searchInputValue.toLowerCase().split(/\s+/);
    for (const sectionId in listItemsCategorised) {
        const section = document.querySelector(`#${sectionId}`);
        const isMatchFoundInSection = searchStaticDatasetEntryListItems(searchInputParts, sectionId);
        if (isMatchFoundInSection) {
            section.classList.remove("d-none");
            continue;
        }
        section.classList.add("d-none");
    }
}

searchInput.addEventListener("input", () => {
    const searchInputValue = searchInput.value;
    if (searchInputValue.trim() === "") {
        return resetSearch();
    }
    return searchCategorySection(searchInputValue);
});

window.addEventListener("load", () => {
    const searchInputValue = searchInput.value;
    if (searchInputValue.trim() !== "") {
        return searchCategorySection(searchInputValue);
    }
});