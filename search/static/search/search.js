/**
 * "Trees" in this context are the top-level class trees from the ESPAS ontology (eventually to become
 * the PITHIA ontology).
 * 
 * The top-level classes from the ontology in this case are "Measurand", "Observed Property",
 * "Phenomenon", "Qualifier".
 * 
 */
const TREE_CONTAINER_IDS = {
    MEASURANDS: "measurands-tree-search-container",
    OBSERVED_PROPERTIES: "observed-properties-tree-search-container",
    PHENOMENONS: "phenomenons-tree-search-container",
    QUALIFIERS: "qualifiers-tree-search-container",
}

const HTML_DATASET_NAMES = {
    MEASURANDS: "measurands",
    OBSERVED_PROPERTIES: "observed-properties",
    PHENOMENONS: "phenomenons",
    QUALIFIERS: "qualifiers",
}

const CHECKBOX_FILTER = "checkboxFilter";
const SEARCH_BOX_INPUT_FILTER = "searchBoxInputFilter";

const UNKNOWN = "unknown"; // because "unknown" is used a lot throughout this code


// Utility functions

function getTreeContainerIdFromInitialSearchFormComponentHTML(htmlText) {
    if (htmlText.includes('name="measurands"')) {
        return TREE_CONTAINER_IDS.MEASURANDS;
    } else if (htmlText.includes('name="observed_properties"')) {
        return TREE_CONTAINER_IDS.OBSERVED_PROPERTIES;
    } else if (htmlText.includes('name="phenomenons"')) {
        return TREE_CONTAINER_IDS.PHENOMENONS;
    } else if (htmlText.includes('name="qualifiers"')) {
        return TREE_CONTAINER_IDS.QUALIFIERS;
    }
    return UNKNOWN;
}

function getHTMLDatasetNameFromTreeContainerId(treeContainerId) {
    switch (treeContainerId) {
        case TREE_CONTAINER_IDS.MEASURANDS: return HTML_DATASET_NAMES.MEASURANDS;
        case TREE_CONTAINER_IDS.OBSERVED_PROPERTIES: return HTML_DATASET_NAMES.OBSERVED_PROPERTIES;
        case TREE_CONTAINER_IDS.PHENOMENONS: return HTML_DATASET_NAMES.PHENOMENONS;
        case TREE_CONTAINER_IDS.QUALIFIERS: return HTML_DATASET_NAMES.QUALIFIERS;
        default: UNKNOWN;
    }
}

function getEnclosingLiNode(elem) {
    let currentParentNode = elem;
    let currentChildNode = elem;
    while (currentParentNode !== null && currentParentNode.nodeName !== "LI") {
        currentParentNode = currentChildNode.parentNode;
        currentChildNode = currentParentNode;
    }
    return currentParentNode;
}

function updateParentNodeCheckboxesByChildNodeCheckbox(childNodeCheckbox) {
    const siblingNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${childNodeCheckbox.dataset.parentNodeInOntology}']`);
    const siblingNodeCheckboxesChecked = document.querySelectorAll(`input[data-parent-node-in-ontology='${childNodeCheckbox.dataset.parentNodeInOntology}']:checked`);
    const parentNodeCheckbox = document.getElementById(childNodeCheckbox.dataset.parentNodeInOntology);
    parentNodeCheckbox.checked = siblingNodeCheckboxes.length === siblingNodeCheckboxesChecked.length;
    if (parentNodeCheckbox.dataset.parentNodeInOntology !== "") {
        updateParentNodeCheckboxesByChildNodeCheckbox(parentNodeCheckbox);
    }
}

function updateChildNodeCheckboxesByParentNodeCheckbox(parentNodeCheckbox) {
    const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${parentNodeCheckbox.id}']`);
    const enclosingLiNode = getEnclosingLiNode(parentNodeCheckbox);
    const childDetailsNodes = enclosingLiNode.querySelectorAll("details");
    childDetailsNodes.forEach(detailsNode => {
        detailsNode.open = true;
    });
    childNodeCheckboxes.forEach(checkbox => {
        checkbox.checked = parentNodeCheckbox.checked;
        const childNodeCheckboxesOfChildNodeCheckbox = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
        if (childNodeCheckboxesOfChildNodeCheckbox.length > 0) {
            updateChildNodeCheckboxesByParentNodeCheckbox(checkbox);
        }
    })
}

// Filtering

function getCheckboxFilteredLiNodesForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.filter-no-match`);
}

function getSearchBoxInputFilteredLiNodesForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.search-no-match`);
}

function getEnclosingLiNodesForCheckboxes(checkboxes) {
    return checkboxes.map(checkbox => getEnclosingLiNode(checkbox));
}

function applyFiltersToLiNodes(filters, liNodes) {
    liNodes.forEach(liNode => {
        if (filters.includes(CHECKBOX_FILTER)) {
            liNode.classList.add("filter-no-match");
        }

        if (filters.includes(SEARCH_BOX_INPUT_FILTER)) {
            liNode.classList.add("search-no-match");
        }
    });
}

function removeFiltersFromLiNodes(filters, liNodes) {
    liNodes.forEach(liNode => {
        if (filters.includes(CHECKBOX_FILTER)) {
            liNode.classList.remove("filter-no-match");
        }

        if (filters.includes(SEARCH_BOX_INPUT_FILTER)) {
            liNode.classList.remove("search-no-match");
        }
    });
}

function filterTreeContainerIdByAnotherTreeContainerId(treeContainerIdToFilter, filterTreeContainerId) {
    const checkboxesToFilterBy = document.querySelectorAll(`#${filterTreeContainerId} input[type="checkbox"]:checked`)
    if (checkboxesToFilterBy.length === 0) {
        const hiddenLisForTreeContainer = getCheckboxFilteredLiNodesForTreeContainerId(treeContainerIdToFilter);
        removeFiltersFromLiNodes([CHECKBOX_FILTER], hiddenLisForTreeContainer);
    } else {
        const ontologyClassDatasetToFilterBy = getHTMLDatasetNameFromTreeContainerId(filterTreeContainerId);
        const checkboxesToFilter = document.querySelectorAll(`#${treeContainerIdToFilter} input[type="checkbox"]`);
        const checkboxesToHide = [], checkboxesToShow = [];
        checkboxesToFilter.forEach(checkboxToFilter => {
            let isCheckboxToFilterAndChildrenVisible = false;
            // OR match
            checkboxesToFilterBy.forEach(checkbox => {
                const ontologyClassDatasetExists = checkboxToFilter.dataset && checkboxToFilter.dataset[ontologyClassDatasetToFilterBy];
                if (ontologyClassDatasetExists && checkboxToFilter.dataset[ontologyClassDatasetToFilterBy].includes(checkbox.id)) {
                    isCheckboxToFilterAndChildrenVisible = true;
                }
            });
            if (isCheckboxToFilterAndChildrenVisible) {
                checkboxesToShow.push(checkboxToFilter);
            } else {
                checkboxesToHide.push(checkboxToFilter);
            }
        });
        const liNodesOfCheckboxesToShow = getEnclosingLiNodesForCheckboxes(checkboxesToShow);
        const liNodesOfCheckboxesToHide = getEnclosingLiNodesForCheckboxes(checkboxesToHide);
        applyFiltersToLiNodes([CHECKBOX_FILTER], liNodesOfCheckboxesToHide);
        removeFiltersFromLiNodes([CHECKBOX_FILTER], liNodesOfCheckboxesToShow);
    }
}

function filterTreeContainerIdBySearchBoxInput(treeContainerId) {
    const allCheckboxLabelsForTree = document.querySelectorAll(`#${treeContainerId} .tree-search-terms label`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxInput = searchBoxForTree.value;
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace
    
    if (searchBoxInput === "") {
        const hiddenLisForTreeContainer = getSearchBoxInputFilteredLiNodesForTreeContainerId(treeContainerIdToFilter);
        removeFiltersFromLiNodes([SEARCH_BOX_INPUT_FILTER], hiddenLisForTreeContainer);
    } else {
        const visibleLiNodes = [], hiddenLiNodes = [];
        allCheckboxLabelsForTree.forEach(label => {
            const enclosingLiNode = getEnclosingLiNode(label);
            // AND match
            let numInputMatchesFound = 0;
            searchBoxInputSplit.forEach(inputTerm => {
                if (label.innerHTML.toLowerCase().includes(inputTerm.toLowerCase())) {
                    numInputMatchesFound++;
                }
            });
            if (numInputMatchesFound === searchBoxInputSplit.length) {
                visibleLiNodes.push(enclosingLiNode);
            } else {
                hiddenLiNodes.push(enclosingLiNode);
            }
        });
        applyFiltersToLiNodes([SEARCH_BOX_INPUT_FILTER], hiddenLiNodes);
        removeFiltersFromLiNodes([SEARCH_BOX_INPUT_FILTER], visibleLiNodes);
    }
}

function resetSearchBoxFilteringForTreeContainerId(treeContainerId) {
    document.querySelector(`#${treeContainerId} .tree-search-box`).value = "";
    const searchBoxInputFilteredLiNodesForTreeContainerId = getSearchBoxInputFilteredLiNodesForTreeContainerId(treeContainerId);
    removeFiltersFromLiNodes([SEARCH_BOX_INPUT_FILTER], searchBoxInputFilteredLiNodesForTreeContainerId);
}

function setCheckboxStatesForTreeContainerId(treeContainerId, checked) {
    return document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`).forEach(checkbox => {
        checkbox.checked = checked;
    });
}

function setDetailsNodeStatesForTreeContainerId(treeContainerId, open) {
    return document.querySelectorAll(`#${treeContainerId} details`).forEach(detailsNode => {
        detailsNode.open = open;
    });
}

function setupInputsForTreeContainer(treeContainerId) {
    const ontologyParentNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"][data-is-parent-node="true"]`);
    ontologyParentNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
            if (childNodeCheckboxes.length > 0) {
                updateChildNodeCheckboxesByParentNodeCheckbox(checkbox);
            }
        });
    });

    const ontologyChildNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]:not([data-parent-node-in-ontology=""])`);
    ontologyChildNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            updateParentNodeCheckboxesByChildNodeCheckbox(checkbox);
        });
    });

    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    searchBoxForTree.addEventListener("input", event => {
        filterTreeContainerIdBySearchBoxInput(treeContainerId);
    });

    const allCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`);
    if (treeContainerId !== TREE_CONTAINER_IDS.OBSERVED_PROPERTIES) {
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                filterTreeContainerIdByAnotherTreeContainerId(TREE_CONTAINER_IDS.OBSERVED_PROPERTIES, treeContainerId);
            });
        });
    }

    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        resetSearchBoxFilteringForTreeContainerId(treeContainerId);
        setCheckboxStatesForTreeContainerId(treeContainerId, false);
        setDetailsNodeStatesForTreeContainerId(treeContainerId, false);
        if (treeContainerId !== TREE_CONTAINER_IDS.OBSERVED_PROPERTIES) {
            const observedPropertyTreeContainerLis = document.querySelectorAll(`#${TREE_CONTAINER_IDS.OBSERVED_PROPERTIES} li`);
            removeFiltersFromLiNodes([CHECKBOX_FILTER], observedPropertyTreeContainerLis);
        }
    });

    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        resetSearchBoxFilteringForTreeContainerId(treeContainerId);
        setCheckboxStatesForTreeContainerId(treeContainerId, true);
        setDetailsNodeStatesForTreeContainerId(treeContainerId, true);
        if (treeContainerId !== TREE_CONTAINER_IDS.OBSERVED_PROPERTIES) {
            filterTreeContainerIdByAnotherTreeContainerId(TREE_CONTAINER_IDS.OBSERVED_PROPERTIES, treeContainerId);
        }
    });
}

async function parseResponseText(response) {
    return response.text();
}

async function loadSearchFormComponent(html) {
    let treeContainerId = getTreeContainerIdFromInitialSearchFormComponentHTML(html);
    if (treeContainerId === UNKNOWN) {
        return console.error("Could not load search form component");
    }
    setTimeout(async () => {
        document.querySelector(`#${treeContainerId} .tree-search-terms`).innerHTML = html;
        setupInputsForTreeContainer(treeContainerId);
        document.querySelector(`#${treeContainerId} .tree-search-terms`).style.opacity = 1;
    }, 300);
    document.querySelector(`#${treeContainerId} .tree-search-terms`).style.opacity = 0;
}

async function loadSearchFormComponents() {
    const fetchParams = { method: "GET" };

    fetch("/search/templates/form/component/measurand/", fetchParams)
        .then(parseResponseText)
        .then(loadSearchFormComponent)
        .catch (error => {
            console.error("Unable to load measurand checkboxes");
            console.error(error);
        });

    fetch("/search/templates/form/component/observedProperty/", fetchParams)
        .then(parseResponseText)
        .then(loadSearchFormComponent)
        .catch (error => {
            console.error("Unable to load observed property checkboxes");
            console.error(error);
        });

    fetch("/search/templates/form/component/phenomenon/", fetchParams)
        .then(parseResponseText)
        .then(loadSearchFormComponent)
        .catch (error => {
            console.error("Unable to load phenomenon checkboxes");
            console.error(error);
        });

    fetch("/search/templates/form/component/qualifier/", fetchParams)
        .then(parseResponseText)
        .then(loadSearchFormComponent)
        .catch (error => {
            console.error("Unable to load qualifier checkboxes");
            console.error(error);
        });
}

document.getElementById("search-script").addEventListener("load", async event => {
    await loadSearchFormComponents();

    const clearInputsButton = document.querySelector(".btn-clear");
    clearInputsButton.addEventListener("click", event => {
        for (const property in TREE_CONTAINER_IDS) {
            const treeContainerId = TREE_CONTAINER_IDS[property];
            resetSearchBoxFilteringForTreeContainerId(treeContainerId);
            setCheckboxStatesForTreeContainerId(treeContainerId, false);
            const checkboxFilteredLiNodesForTreeContainerId = getCheckboxFilteredLiNodesForTreeContainerId(treeContainerId);
            removeFiltersFromLiNodes([CHECKBOX_FILTER], checkboxFilteredLiNodesForTreeContainerId);
            setDetailsNodeStatesForTreeContainerId(treeContainerId, false);
        }
    });
});