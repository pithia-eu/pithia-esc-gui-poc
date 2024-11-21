import {
    setupCheckboxesForTreeContainerIdToFilterOPTerms,
    setupSelectAllButtonForTreeContainerId,
    activateDeselectAllButtonForTreeContainerId,
} from "/static/search/opsearch.js";

import {
    addTreeContainerIdToClearInputsButton,
    fetchSearchFormComponent,
    setupSearchFormComponent
} from "./search.js";

const COMPUTATION_TYPES_TREE_CONTAINER_ID = "computation-types-tree-search-container";
const INSTRUMENT_TYPES_TREE_CONTAINER_ID = "instrument-types-tree-search-container";
const ANNOTATION_TYPES_TREE_CONTAINER_ID = "annotation-types-tree-search-container";
const clearTypeInputsButton = document.querySelector(".btn-clear-type-inputs");


async function fetchAndSetupSearchFormComponents() {
    const searchFormComponents = await Promise.all([
        fetchSearchFormComponent("computationType"),
        fetchSearchFormComponent("instrumentType"),
        fetchSearchFormComponent("annotationType"),
    ]);
    setupSearchFormComponent(searchFormComponents[0], COMPUTATION_TYPES_TREE_CONTAINER_ID, () => {
        // setupCheckboxesForTreeContainerIdToFilterOPTerms(COMPUTATION_TYPES_TREE_CONTAINER_ID);
        // setupSelectAllButtonForTreeContainerId(COMPUTATION_TYPES_TREE_CONTAINER_ID);
        // activateDeselectAllButtonForTreeContainerId(COMPUTATION_TYPES_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(COMPUTATION_TYPES_TREE_CONTAINER_ID, clearTypeInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[1], INSTRUMENT_TYPES_TREE_CONTAINER_ID, () => {
        // setupCheckboxesForTreeContainerIdToFilterOPTerms(INSTRUMENT_TYPES_TREE_CONTAINER_ID);
        // setupSelectAllButtonForTreeContainerId(INSTRUMENT_TYPES_TREE_CONTAINER_ID);
        // activateDeselectAllButtonForTreeContainerId(INSTRUMENT_TYPES_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(INSTRUMENT_TYPES_TREE_CONTAINER_ID, clearTypeInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[2], ANNOTATION_TYPES_TREE_CONTAINER_ID, () => {
        // setupCheckboxesForTreeContainerIdToFilterOPTerms(ANNOTATION_TYPES_TREE_CONTAINER_ID);
        // setupSelectAllButtonForTreeContainerId(ANNOTATION_TYPES_TREE_CONTAINER_ID);
        // activateDeselectAllButtonForTreeContainerId(ANNOTATION_TYPES_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(ANNOTATION_TYPES_TREE_CONTAINER_ID, clearTypeInputsButton);
    });
}


document.getElementById("typesearch-script").addEventListener("load", async event => {
    await fetchAndSetupSearchFormComponents();
});