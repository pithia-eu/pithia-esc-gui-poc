import {
    setupSearchFormComponent
} from "/static/search/search.js";

const FEATURES_OF_INTEREST_TREE_CONTAINER_ID = "features-of-interest-tree-search-container";


async function fetchFeatureOfInterestForm() {
    const fetchParams = { method: "GET" };

    try {
        const response = await fetch(`/static-dataset-search/templates/foi-form/`, fetchParams)
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