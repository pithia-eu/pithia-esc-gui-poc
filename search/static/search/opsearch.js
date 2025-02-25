import {
    addCheckboxFiltersToLiNodes,
    addTreeContainerIdToClearInputsButton,
    fetchSearchFormComponent,
    getEnclosingLiNode,
    getLiNodesHiddenByCheckboxFilterForTreeContainerId,
    getParentNodeCheckboxes,
    getSearchTermsContainerForTreeContainerId,
    getSelectAllCheckboxForTreeContainerId,
    removeCheckboxFiltersFromLiNodes,
    setupSearchFormComponent,
} from "./search.js";

// op, OP = Observed Property
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
        setupCheckboxesForTreeContainerIdToFilterOPTerms(MEASURANDS_TREE_CONTAINER_ID);
        setupSelectAllCheckboxForTreeContainerId(MEASURANDS_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(MEASURANDS_TREE_CONTAINER_ID, clearObservedPropertiesInputsButton);
    });
    setupSearchFormComponent(searchFormComponents[2], PHENOMENONS_TREE_CONTAINER_ID, () => {
        setupCheckboxesForTreeContainerIdToFilterOPTerms(PHENOMENONS_TREE_CONTAINER_ID);
        setupSelectAllCheckboxForTreeContainerId(PHENOMENONS_TREE_CONTAINER_ID);
        addTreeContainerIdToClearInputsButton(PHENOMENONS_TREE_CONTAINER_ID, clearObservedPropertiesInputsButton);
    });
}

function getHtmlDatasetNameByInputName(inputName) {
    switch (inputName) {
        case 'phenomenon': return 'phenomenons';
        case 'measurand': return 'measurands';
        default: 'unknown';
    }
}

function hideShownAndHiddenNumbersForOpTree() {
    const checkboxFilterResultsElementContainer = document.querySelector(`#${OBSERVED_PROPERTIES_TREE_CONTAINER_ID}`).querySelector(".tree-filter-results");
    return checkboxFilterResultsElementContainer.classList.remove("show-tree-checkbox-filter-results");
}

function showAndUpdateShownAndHiddenNumbersForOpTree(checkboxesHidden, checkboxesShown) {
    const checkboxFilterResultsElement = document.querySelector(`#${OBSERVED_PROPERTIES_TREE_CONTAINER_ID}`).querySelector(".tree-checkbox-filter-results");
    checkboxFilterResultsElement.textContent = `${checkboxesShown.length} filtered, ${checkboxesHidden.length} made less visible by phenomenons/measurands`;
    const checkboxFilterResultsElementContainer = document.querySelector(`#${OBSERVED_PROPERTIES_TREE_CONTAINER_ID}`).querySelector(".tree-filter-results");
    return checkboxFilterResultsElementContainer.classList.add("show-tree-checkbox-filter-results");
}

function filterOpTree() {
    const checkedPhenomenonCheckboxes = Array.from(getSearchTermsContainerForTreeContainerId(PHENOMENONS_TREE_CONTAINER_ID).querySelectorAll(`input[type="checkbox"]:checked`));
    const checkedMeasurandCheckboxes= Array.from(getSearchTermsContainerForTreeContainerId(MEASURANDS_TREE_CONTAINER_ID).querySelectorAll(`input[type="checkbox"]:checked`));
    const checkboxesToFilterBy = checkedPhenomenonCheckboxes.concat(checkedMeasurandCheckboxes);
    if (checkboxesToFilterBy.length === 0) {
        const hiddenLisForTreeContainer = getLiNodesHiddenByCheckboxFilterForTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID);
        hideShownAndHiddenNumbersForOpTree();
        return removeCheckboxFiltersFromLiNodes(hiddenLisForTreeContainer);
    }
    const checkboxesToFilter = getSearchTermsContainerForTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID).querySelectorAll(`input[type="checkbox"]`);
    const liNodesToHide = [], liNodesToShow = [];
    const checkboxesShown = [], checkboxesHidden = [];
    checkboxesToFilter.forEach(checkboxToFilter => {
        // OR match
        const enclosingLiNode = getEnclosingLiNode(checkboxToFilter);
        for (const checkboxToFilterBy of checkboxesToFilterBy) {
            const htmlDatasetToFilterBy = getHtmlDatasetNameByInputName(checkboxToFilterBy.name);
            const isHtmlDatasetInCheckbox = checkboxToFilter.dataset && checkboxToFilter.dataset[htmlDatasetToFilterBy];
            if (isHtmlDatasetInCheckbox && checkboxToFilter.dataset[htmlDatasetToFilterBy].includes(checkboxToFilterBy.id)) {
                liNodesToShow.push(enclosingLiNode);
                const parentCheckboxes = getParentNodeCheckboxes(checkboxToFilter);
                const parentLiNodesToShow = parentCheckboxes.map(checkbox => getEnclosingLiNode(checkbox));
                liNodesToShow.push(...parentLiNodesToShow);
                if (!checkboxToFilter.disabled) {
                    checkboxesShown.push(checkboxToFilter);
                }
                return;
            }
        }
        if (!checkboxToFilter.disabled) {
            checkboxesHidden.push(checkboxToFilter);
        }
        return liNodesToHide.push(enclosingLiNode);
    });
    showAndUpdateShownAndHiddenNumbersForOpTree(checkboxesHidden, checkboxesShown);
    addCheckboxFiltersToLiNodes(liNodesToHide);
    removeCheckboxFiltersFromLiNodes(liNodesToShow);
}

export function setupCheckboxesForTreeContainerIdToFilterOPTerms(treeContainerId) {
    const allCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`);
    allCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            filterOpTree();
        });
    });
}

export function setupSelectAllCheckboxForTreeContainerId(treeContainerId) {
    const selectAllCheckbox = getSelectAllCheckboxForTreeContainerId(treeContainerId);
    selectAllCheckbox.addEventListener("change", event => {
        filterOpTree();
    });
}

export function activateDeselectAllButtonForTreeContainerId(treeContainerId) {
    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        filterOpTree();
    });
}

export function setupSelectAllButtonForTreeContainerId(treeContainerId) {
    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        filterOpTree();
    });
}


document.getElementById("opsearch-script").addEventListener("load", async event => {
    await fetchAndSetupSearchFormComponents();
});