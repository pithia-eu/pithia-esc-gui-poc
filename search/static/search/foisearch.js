import {
    addTreeContainerIdToClearInputsButton,
    fetchSearchFormComponent,
    setupSearchFormComponent
} from "./search.js";

const FEATURES_OF_INTEREST_TREE_CONTAINER_ID = "features-of-interest-tree-search-container";


async function fetchAndSetupFeatureOfInterestForm() {
    const featureOfInterestForm = await fetchSearchFormComponent("featureOfInterest");
    setupSearchFormComponent(featureOfInterestForm, FEATURES_OF_INTEREST_TREE_CONTAINER_ID);
}

document.getElementById("foisearch-script").addEventListener("load", async event => {
    await fetchAndSetupFeatureOfInterestForm();
});