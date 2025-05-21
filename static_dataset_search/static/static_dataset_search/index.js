import {
    setupSearchFormComponent
} from "/static/search/search.js";

const featureOfInterestFormUrl = JSON.parse(document.querySelector("#feature-of-interest-form-url").textContent);
const FEATURES_OF_INTEREST_TREE_CONTAINER_ID = "features-of-interest-tree-search-container";


async function fetchFeatureOfInterestForm() {
    const fetchParams = { method: "GET" };

    try {
        const response = await fetch(featureOfInterestFormUrl, fetchParams)
        return response.text();
    } catch (error) {
        console.error(`Unable to fetch search form.`);
        console.error(error);
    }
}

async function fetchAndSetupFeatureOfInterestForm() {
    const featureOfInterestForm = await fetchFeatureOfInterestForm();
    setupSearchFormComponent(featureOfInterestForm, FEATURES_OF_INTEREST_TREE_CONTAINER_ID);
}

document.getElementById("search-script").addEventListener("load", async event => {
    await fetchAndSetupFeatureOfInterestForm();
});

document.getElementById("ontology-search-form").addEventListener("submit", event => {
    const checkedCheckboxes = document.querySelectorAll("#ontology-search-form input[type=checkbox].search-term-checkbox:checked");
    if (checkedCheckboxes.length === 0) {
        event.preventDefault();
        return alert('Select at least one Feature of Interest.');
    }
});