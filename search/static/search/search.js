const CHECKBOX_FILTER_CLASS = "filter-no-match";
const SEARCH_BOX_INPUT_FILTER_CLASS = "search-no-match";


// Utility functions

export function getEnclosingLiNode(elem) {
    let currentParentNode = elem;
    let currentChildNode = elem;
    while (currentParentNode !== null && currentParentNode.nodeName !== "LI") {
        currentParentNode = currentChildNode.parentNode;
        currentChildNode = currentParentNode;
    }
    return currentParentNode;
}

export function getParentNodeCheckboxes(checkbox, parentNodeCheckboxes) {
    if (!parentNodeCheckboxes) {
        parentNodeCheckboxes = [];
    }
    if (checkbox.dataset.parentNodeInOntology === "") {
        return parentNodeCheckboxes;
    }
    const parentNodeCheckbox = document.getElementById(checkbox.dataset.parentNodeInOntology);
    parentNodeCheckboxes.push(parentNodeCheckbox);
    if (parentNodeCheckbox.dataset.parentNodeInOntology !== "") {
        parentNodeCheckboxes = getParentNodeCheckboxes(parentNodeCheckbox, parentNodeCheckboxes);
    }
    return parentNodeCheckboxes;
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


// Checkbox filtering

export function getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.filter-no-match`);
}

function addCheckboxFilterToLiNode(liNode) {
    liNode.classList.add(CHECKBOX_FILTER_CLASS);
}

function removeCheckboxFilterFromLiNode(liNode) {
    liNode.classList.remove(CHECKBOX_FILTER_CLASS);
}

export function addCheckboxFiltersToLiNodes(liNodes) {
    liNodes.forEach(liNode => {
        addCheckboxFilterToLiNode(liNode);
    });
}

export function removeCheckboxFiltersFromLiNodes(liNodes) {
    liNodes.forEach(liNode => {
        removeCheckboxFilterFromLiNode(liNode);
    });
}

// Search box input filtering

function getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId) {
    return document.querySelectorAll(`#${treeContainerId} li.search-no-match`);
}

function addSearchBoxInputFilterToLiNode(liNode) {
    liNode.classList.add(SEARCH_BOX_INPUT_FILTER_CLASS);
}

function removeSearchBoxInputFilterFromLiNode(liNode) {
    liNode.classList.remove(SEARCH_BOX_INPUT_FILTER_CLASS);
}

function addSearchBoxInputFiltersToLiNodes(liNodes) {
    liNodes.forEach(liNode => {
        addSearchBoxInputFilterToLiNode(liNode);
    });
}

function removeSearchBoxInputFiltersFromLiNodes(liNodes) {
    liNodes.forEach(liNode => {
        removeSearchBoxInputFilterFromLiNode(liNode);
    });
}

function filterTreeContainerIdBySearchBoxInput(treeContainerId) {
    const allCheckboxLabelsForTree = document.querySelectorAll(`#${treeContainerId} .tree-search-terms label`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxInput = searchBoxForTree.value;
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace
    
    if (searchBoxInput === "") {
        const hiddenLisForTreeContainer = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId);
        removeSearchBoxInputFiltersFromLiNodes(hiddenLisForTreeContainer);
    } else {
        let liNodesToShow = [], liNodesToHide = [];
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
                const childNodeCheckboxes = enclosingLiNode.getElementsByTagName("input");
                if (childNodeCheckboxes.length > 0) {
                    const firstChildNodeCheckbox = childNodeCheckboxes[0];
                    const parentNodeCheckboxes = getParentNodeCheckboxes(firstChildNodeCheckbox);
                    parentNodeCheckboxes.forEach(checkbox => {
                        const enclosingLiNodeOfParentNodeCheckbox = getEnclosingLiNode(checkbox);
                        liNodesToShow.push(enclosingLiNodeOfParentNodeCheckbox);
                    });
                }
            } else {
                liNodesToHide.push(enclosingLiNode);
            }
        });
        liNodesToHide = Array.from(new Set(liNodesToHide));
        liNodesToShow = Array.from(new Set(liNodesToShow));
        addSearchBoxInputFiltersToLiNodes(liNodesToHide);
        removeSearchBoxInputFiltersFromLiNodes(liNodesToShow);
    }
}

function resetSearchBoxFilteringForTreeContainerId(treeContainerId) {
    document.querySelector(`#${treeContainerId} .tree-search-box`).value = "";
    const searchBoxInputFilteredLiNodesForTreeContainerId = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId);
    removeSearchBoxInputFiltersFromLiNodes(searchBoxInputFilteredLiNodesForTreeContainerId);
}

function setCheckboxCheckedStatesForTreeContainerId(treeContainerId, checked) {
    return document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`).forEach(checkbox => {
        checkbox.checked = checked;
    });
}

function setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, open) {
    return document.querySelectorAll(`#${treeContainerId} details`).forEach(detailsNode => {
        detailsNode.open = open;
    });
}

export function checkAllCheckboxesForTreeContainerId(treeContainerId, allCheckboxesChecked) {
    resetSearchBoxFilteringForTreeContainerId(treeContainerId);
    setCheckboxCheckedStatesForTreeContainerId(treeContainerId, allCheckboxesChecked);
    setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, allCheckboxesChecked);
}

function setupInputsForTreeContainerId(treeContainerId) {
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

    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        checkAllCheckboxesForTreeContainerId(treeContainerId, false);
    });

    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        checkAllCheckboxesForTreeContainerId(treeContainerId, true);
    });
}

// Search form setup

export function addTreeContainerIdToClearInputsButton(treeContainerId) {
    const clearInputsButton = document.querySelector(".btn-clear");
    clearInputsButton.addEventListener("click", event => {
        checkAllCheckboxesForTreeContainerId(treeContainerId, false);
        const checkboxFilteredLiNodesForTreeContainerId = getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerId);
        removeCheckboxFiltersFromLiNodes(checkboxFilteredLiNodesForTreeContainerId);
    });
}

export async function setupSearchFormComponent(html, treeContainerId, callback) {
    setTimeout(async () => {
        document.querySelector(`#${treeContainerId} .tree-search-terms`).innerHTML = html;
        setupInputsForTreeContainerId(treeContainerId);
        document.querySelector(`#${treeContainerId} .tree-search-terms`).style.opacity = 1;
        if (callback) {
            callback();
        }
    }, 300);
    document.querySelector(`#${treeContainerId} .tree-search-terms`).style.opacity = 0;
}

async function parseResponseText(response) {
    return response.text();
}

export async function fetchSearchFormComponent(ontologyComponent) {
    const fetchParams = { method: "GET" };

    return fetch(`/search/templates/form/component/${ontologyComponent}/`, fetchParams)
        .then(parseResponseText)
        .catch (error => {
            console.error(`Unable to fetch ${ontologyComponent} search form.`);
            console.error(error);
        });
}