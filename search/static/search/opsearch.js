import {
    addCheckboxFiltersToLiNodes,
    addTreeContainerIdToClearInputsButton,
    fetchSearchFormComponent,
    getEnclosingLiNode,
    getLiNodesHiddenByCheckboxFilterForTreeContainerId,
    getParentNodeCheckboxes,
    removeCheckboxFiltersFromLiNodes,
    setupSearchFormComponent
} from "./search.js";

const OBSERVED_PROPERTIES_TREE_CONTAINER_ID = "observed-properties-tree-search-container";
const MEASURANDS_TREE_CONTAINER_ID = "measurands-tree-search-container";
const PHENOMENONS_TREE_CONTAINER_ID = "phenomenons-tree-search-container";
const INSTRUMENT_TYPES_TREE_CONTAINER_ID = "instrument-types-tree-search-container";
const COMPUTATION_TYPES_TREE_CONTAINER_ID = "computation-types-tree-search-container";
const clearObservedPropertiesInputsButton = document.querySelector(".btn-clear-op-inputs");

async function fetchAndSetupSearchFormComponents() {
    const searchFormComponents = await Promise.all([
        fetchSearchFormComponent("observedProperty"),
        fetchSearchFormComponent("measurand"),
        fetchSearchFormComponent("phenomenon"),
    ]);
    setupSearchFormComponent(searchFormComponents[0], OBSERVED_PROPERTIES_TREE_CONTAINER_ID, () => {
        addTreeContainerIdToClearInputsButton(OBSERVED_PROPERTIES_TREE_CONTAINER_ID, clearObservedPropertiesInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[1], MEASURANDS_TREE_CONTAINER_ID, () => {
        setupObservedPropertiesTreeFilteringForTreeContainerId(MEASURANDS_TREE_CONTAINER_ID);
        setupSelectAllButtonForTreeContainerId(MEASURANDS_TREE_CONTAINER_ID);
        setupDeselectAllButtonForTreeContainerId(MEASURANDS_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(MEASURANDS_TREE_CONTAINER_ID, clearObservedPropertiesInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[2], PHENOMENONS_TREE_CONTAINER_ID, () => {
        setupObservedPropertiesTreeFilteringForTreeContainerId(PHENOMENONS_TREE_CONTAINER_ID);
        setupSelectAllButtonForTreeContainerId(PHENOMENONS_TREE_CONTAINER_ID);
        setupDeselectAllButtonForTreeContainerId(PHENOMENONS_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(PHENOMENONS_TREE_CONTAINER_ID, clearObservedPropertiesInputsButton);
    });
}

function getHTMLDatasetNameFromTreeContainerId(treeContainerId) {
    switch (treeContainerId) {
        case MEASURANDS_TREE_CONTAINER_ID: return "measurands";
        case OBSERVED_PROPERTIES_TREE_CONTAINER_ID: return "observedProperties";
        case PHENOMENONS_TREE_CONTAINER_ID: return "phenomenons";
        case INSTRUMENT_TYPES_TREE_CONTAINER_ID: return "instrumentTypes";
        case COMPUTATION_TYPES_TREE_CONTAINER_ID: return "computationTypes";
        default: UNKNOWN;
    }
}

function filterTreeContainerIdByAnotherTreeContainerId(treeContainerIdToFilter, filterTreeContainerId) {
    const checkboxesToFilterBy = document.querySelectorAll(`#${filterTreeContainerId} input[type="checkbox"]:checked`)
    console.log("checkboxesToFilterBy", checkboxesToFilterBy);
    if (checkboxesToFilterBy.length === 0) {
        const hiddenLisForTreeContainer = getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerIdToFilter);
        removeCheckboxFiltersFromLiNodes(hiddenLisForTreeContainer);
    } else {
        const ontologyClassDatasetToFilterBy = getHTMLDatasetNameFromTreeContainerId(filterTreeContainerId);
        const checkboxesToFilter = document.querySelectorAll(`#${treeContainerIdToFilter} input[type="checkbox"]`);
        const liNodesToHide = [], liNodesToShow = [];
        checkboxesToFilter.forEach(checkboxToFilter => {
            let isCheckboxToFilterAndChildrenVisible = false;
            // OR match
            checkboxesToFilterBy.forEach(checkbox => {
                const ontologyClassDatasetExists = checkboxToFilter.dataset && checkboxToFilter.dataset[ontologyClassDatasetToFilterBy];
                if (ontologyClassDatasetExists && checkboxToFilter.dataset[ontologyClassDatasetToFilterBy].includes(checkbox.id)) {
                    isCheckboxToFilterAndChildrenVisible = true;
                }
            });
            const enclosingLiNode = getEnclosingLiNode(checkboxToFilter);
            if (isCheckboxToFilterAndChildrenVisible) {
                liNodesToShow.push(enclosingLiNode);
                const parentCheckboxes = getParentNodeCheckboxes(checkboxToFilter);
                const parentLiNodesToShow = parentCheckboxes.map(checkbox => getEnclosingLiNode(checkbox));
                liNodesToShow.push(...parentLiNodesToShow);
            } else {
                liNodesToHide.push(enclosingLiNode);
            }
        });
        addCheckboxFiltersToLiNodes(liNodesToHide);
        removeCheckboxFiltersFromLiNodes(liNodesToShow);
    }
}

export function setupObservedPropertiesTreeFilteringForTreeContainerId(treeContainerId) {
    const allCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`);
    allCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            filterTreeContainerIdByAnotherTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID, treeContainerId);
        });
    });
}

function setupDeselectAllButtonForTreeContainerId(treeContainerId) {
    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        const observedPropertiesTreeContainerLis = document.querySelectorAll(`#${OBSERVED_PROPERTIES_TREE_CONTAINER_ID} li`);
        removeCheckboxFiltersFromLiNodes(observedPropertiesTreeContainerLis);
    });
}

function setupSelectAllButtonForTreeContainerId(treeContainerId) {
    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        filterTreeContainerIdByAnotherTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID, treeContainerId);
    });
}


document.getElementById("opsearch-script").addEventListener("load", async event => {
    await fetchAndSetupSearchFormComponents();
});