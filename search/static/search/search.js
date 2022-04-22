/**
 * "Trees" in this context are the top-level class trees from the ESPAS ontology (eventually to become
 * the PITHIA ontology).
 * 
 * The top-level classes from the ontology in this case are "Measurand", "Observed Property",
 * "Phenomenon", "Qualifier".
 * 
 */
const MEASURANDS_TREE_CONTAINER_ID = "measurands-tree-search-container";
const OBSERVED_PROPERTIES_TREE_CONTAINER_ID = "observed-properties-tree-search-container";
const PHENOMENONS_TREE_CONTAINER_ID = "phenomenons-tree-search-container";
const QUALIFIERS_TREE_CONTAINER_ID = "qualifiers-tree-search-container";

const CHECKBOX_FILTER_CLASS = "filter-no-match";
const SEARCH_BOX_INPUT_FILTER_CLASS = "search-no-match";

const UNKNOWN = "unknown"; // because "unknown" is used a lot throughout this code


// Utility functions

function getTreeContainerIdFromInitialSearchFormComponentHTML(htmlText) {
    if (htmlText.includes('name="measurands"')) {
        return MEASURANDS_TREE_CONTAINER_ID;
    } else if (htmlText.includes('name="observed_properties"')) {
        return OBSERVED_PROPERTIES_TREE_CONTAINER_ID;
    } else if (htmlText.includes('name="phenomenons"')) {
        return PHENOMENONS_TREE_CONTAINER_ID;
    } else if (htmlText.includes('name="qualifiers"')) {
        return QUALIFIERS_TREE_CONTAINER_ID;
    }
    return UNKNOWN;
}

function getHTMLDatasetNameFromTreeContainerId(treeContainerId) {
    switch (treeContainerId) {
        case MEASURANDS_TREE_CONTAINER_ID: return "measurands";
        case OBSERVED_PROPERTIES_TREE_CONTAINER_ID: return "observed-properties";
        case PHENOMENONS_TREE_CONTAINER_ID: return "phenomenons";
        case QUALIFIERS_TREE_CONTAINER_ID: return "qualifiers";
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

function getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.filter-no-match`);
}

function getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.search-no-match`);
}

function addFilterClassesToLiNodes(filters, liNodes) {
    liNodes.forEach(liNode => {
        if (filters.includes(CHECKBOX_FILTER_CLASS)) {
            liNode.classList.add(CHECKBOX_FILTER_CLASS);
        }

        if (filters.includes(SEARCH_BOX_INPUT_FILTER_CLASS)) {
            liNode.classList.add(SEARCH_BOX_INPUT_FILTER_CLASS);
        }
    });
}

function removeFilterClassesFromLiNodes(filters, liNodes) {
    liNodes.forEach(liNode => {
        if (filters.includes(CHECKBOX_FILTER_CLASS)) {
            liNode.classList.remove(CHECKBOX_FILTER_CLASS);
        }

        if (filters.includes(SEARCH_BOX_INPUT_FILTER_CLASS)) {
            liNode.classList.remove(SEARCH_BOX_INPUT_FILTER_CLASS);
        }
    });
}

function filterTreeContainerIdByAnotherTreeContainerId(treeContainerIdToFilter, filterTreeContainerId) {
    const checkboxesToFilterBy = document.querySelectorAll(`#${filterTreeContainerId} input[type="checkbox"]:checked`)
    if (checkboxesToFilterBy.length === 0) {
        const hiddenLisForTreeContainer = getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerIdToFilter);
        removeFilterClassesFromLiNodes([CHECKBOX_FILTER_CLASS], hiddenLisForTreeContainer);
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
            const enclosingLiNode = getEnclosingLiNode(label);
            if (isCheckboxToFilterAndChildrenVisible) {
                liNodesToShow.push(enclosingLiNode);
            } else {
                liNodesToHide.push(enclosingLiNode);
            }
        });
        addFilterClassesToLiNodes([CHECKBOX_FILTER_CLASS], liNodesToHide);
        removeFilterClassesFromLiNodes([CHECKBOX_FILTER_CLASS], liNodesToShow);
    }
}

function filterTreeContainerIdBySearchBoxInput(treeContainerId) {
    const allCheckboxLabelsForTree = document.querySelectorAll(`#${treeContainerId} .tree-search-terms label`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxInput = searchBoxForTree.value;
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace
    
    if (searchBoxInput === "") {
        const hiddenLisForTreeContainer = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerIdToFilter);
        removeFilterClassesFromLiNodes([SEARCH_BOX_INPUT_FILTER_CLASS], hiddenLisForTreeContainer);
    } else {
        const liNodesToShow = [], liNodesToHide = [];
        allCheckboxLabelsForTree.forEach(label => {
            // AND match
            let numInputMatchesFound = 0;
            searchBoxInputSplit.forEach(inputTerm => {
                if (label.innerHTML.toLowerCase().includes(inputTerm.toLowerCase())) {
                    numInputMatchesFound++;
                }
            });
            const enclosingLiNode = getEnclosingLiNode(label);
            if (numInputMatchesFound === searchBoxInputSplit.length) {
                liNodesToShow.push(enclosingLiNode);
            } else {
                liNodesToHide.push(enclosingLiNode);
            }
        });
        addFilterClassesToLiNodes([SEARCH_BOX_INPUT_FILTER_CLASS], liNodesToHide);
        removeFilterClassesFromLiNodes([SEARCH_BOX_INPUT_FILTER_CLASS], liNodesToShow);
    }
}

function resetSearchBoxFilteringForTreeContainerId(treeContainerId) {
    document.querySelector(`#${treeContainerId} .tree-search-box`).value = "";
    const searchBoxInputFilteredLiNodesForTreeContainerId = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId);
    removeFilterClassesFromLiNodes([SEARCH_BOX_INPUT_FILTER_CLASS], searchBoxInputFilteredLiNodesForTreeContainerId);
}

function setTreeContainerSelectionById(treeContainerId, selectAll) {
    resetSearchBoxFilteringForTreeContainerId(treeContainerId);
    setCheckboxStatesForTreeContainerId(treeContainerId, selectAll);
    setDetailsNodeStatesForTreeContainerId(treeContainerId, selectAll);
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
    if (treeContainerId !== OBSERVED_PROPERTIES_TREE_CONTAINER_ID) {
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                filterTreeContainerIdByAnotherTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID, treeContainerId);
            });
        });
    }

    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        setTreeContainerSelectionById(treeContainerId, false);
        if (treeContainerId !== OBSERVED_PROPERTIES_TREE_CONTAINER_ID) {
            const observedPropertyTreeContainerLis = document.querySelectorAll(`#${OBSERVED_PROPERTIES_TREE_CONTAINER_ID} li`);
            removeFilterClassesFromLiNodes([CHECKBOX_FILTER_CLASS], observedPropertyTreeContainerLis);
        }
    });

    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        setTreeContainerSelectionById(treeContainerId, true);
        if (treeContainerId !== OBSERVED_PROPERTIES_TREE_CONTAINER_ID) {
            filterTreeContainerIdByAnotherTreeContainerId(OBSERVED_PROPERTIES_TREE_CONTAINER_ID, treeContainerId);
        }
    });
}

// Search form setup

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
        const treeContainerIds = [
            MEASURANDS_TREE_CONTAINER_ID,
            OBSERVED_PROPERTIES_TREE_CONTAINER_ID,
            PHENOMENONS_TREE_CONTAINER_ID,
            QUALIFIERS_TREE_CONTAINER_ID,
        ];
        for (const treeContainerId in treeContainerIds) {
            setTreeContainerSelectionById(treeContainerId, false);
            const checkboxFilteredLiNodesForTreeContainerId = getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerId);
            removeFilterClassesFromLiNodes([CHECKBOX_FILTER_CLASS], checkboxFilteredLiNodesForTreeContainerId);
        }
    });
});