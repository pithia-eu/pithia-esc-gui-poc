import {
    fetchSearchFormComponent,
    setupSearchFormComponent
} from "/static/search/search.js";


const featureOfInterestFormUrl = JSON.parse(document.querySelector("#feature-of-interest-form-url").textContent);
const FEATURES_OF_INTEREST_TREE_CONTAINER_ID = "features-of-interest-tree-search-container";


async function fetchAndSetupFeatureOfInterestForm() {
    const featureOfInterestForm = await fetchSearchFormComponent(featureOfInterestFormUrl);
    setupSearchFormComponent(featureOfInterestForm, FEATURES_OF_INTEREST_TREE_CONTAINER_ID);
}

document.getElementById("foisearch-script").addEventListener("load", async event => {
    await fetchAndSetupFeatureOfInterestForm();
});