import {
    filterResourceList,
} from "/static/browse/resource_filter_by_name_setup.js";

const searchInput = document.querySelector("#resource-name-search");
const searchableList = document.querySelector(".list-group-searchable");
const searchableListItemText = Array.from(searchableList.children).reduce(
    (accumulator, currentValue) => {
        accumulator[currentValue.id] = currentValue.textContent.trim();
        return accumulator;
    },
    {}
);
const searchableListClone = searchableList.cloneNode(true);

const resourceListCount = document.querySelector("#resource-list-count");
const typeReadable = JSON.parse(document.querySelector("#type-readable").textContent);
const typePluralReadable = JSON.parse(document.querySelector("#type-plural-readable").textContent);


function filterResourcesListDefault() {
    filterResourceList(
        searchInput,
        searchableList,
        searchableListClone,
        searchableListItemText,
        resourceListCount,
        typeReadable,
        typePluralReadable
    );
}

searchInput.addEventListener("input", () => {
    filterResourcesListDefault();
});

window.addEventListener("load", () => {
    filterResourcesListDefault();
});