import {
    addTreeContainerIdToClearInputsButton,
    fetchSearchFormComponent,
    setupSearchFormComponent
} from "./search.js";

const COMPUTATION_TYPES_TREE_CONTAINER_ID = "computation-types-tree-search-container";
const INSTRUMENT_TYPES_TREE_CONTAINER_ID = "instrument-types-tree-search-container";
const clearTypeInputsButton = document.querySelector(".btn-clear-type-inputs");


async function fetchAndSetupSearchFormComponents() {
    const searchFormComponents = await Promise.all([
        fetchSearchFormComponent("computationType"),
        fetchSearchFormComponent("instrumentType"),
    ]);
    setupSearchFormComponent(searchFormComponents[0], COMPUTATION_TYPES_TREE_CONTAINER_ID, () => {
        addTreeContainerIdToClearInputsButton(COMPUTATION_TYPES_TREE_CONTAINER_ID, clearTypeInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[1], INSTRUMENT_TYPES_TREE_CONTAINER_ID, () => {
        addTreeContainerIdToClearInputsButton(INSTRUMENT_TYPES_TREE_CONTAINER_ID, clearTypeInputsButton);
    });
}


document.getElementById("typesearch-script").addEventListener("load", async event => {
    await fetchAndSetupSearchFormComponents();
});