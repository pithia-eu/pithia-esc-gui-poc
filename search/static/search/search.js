const CHECKBOX_FILTER_CLASS = "filter-no-match";
const SEARCH_BOX_INPUT_FILTER_CLASS = "search-no-match";


// Filtering utility functions

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
    return getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`li.filter-no-match`);
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
    return getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`li.search-no-match`);
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
    const allCheckboxLabelsForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`label`);
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

        // Collapse hidden nodes, expand visible ones
        setDetailNodeOpenStatesForLiNodes(liNodesToShow, true);
        setDetailNodeOpenStatesForLiNodes(liNodesToHide, false);
    }
}

// Utility functions

function getSearchTermsContainerForTreeContainerId(treeContainerId) {
    return document.querySelector(`#${treeContainerId} .tree-search-terms`);
}

function getCheckboxesForTreeContainerId(treeContainerId) {
    return Array.from(getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:not([disabled])`));
}

function getSelectAllCheckboxForTreeContainerId(treeContainerId) {
    return document.querySelector(`#${treeContainerId} input[type="checkbox"][id$="select-all-checkbox"]`);
}

function getSelectAllCheckboxLabelForTreeContainerId(treeContainerId) {
    return document.querySelector(`#${treeContainerId} label[for$="select-all-checkbox"]`);
}

function getCheckboxCheckedStateForTreeContainerId(treeContainerId) {
    const allCheckedCheckboxes = Array.from(getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:checked:not([disabled])`));
    const allEnabledCheckboxesForTreeContainerId = getCheckboxesForTreeContainerId(treeContainerId);
    if (allEnabledCheckboxesForTreeContainerId.length == allCheckedCheckboxes.length) {
        return 'all';
    } else if (allCheckedCheckboxes.length == 0) {
        return 'none';
    }
    return 'indeterminate';
}

function setSelectAllCheckboxForTreeContainerId(treeContainerId) {
    const treeContainerCheckedState = getCheckboxCheckedStateForTreeContainerId(treeContainerId);
    const selectAllCheckbox = getSelectAllCheckboxForTreeContainerId(treeContainerId);
    selectAllCheckbox.indeterminate = false;
    if (treeContainerCheckedState == 'all') {
        return selectAllCheckbox.checked = true;
    } else if (treeContainerCheckedState == 'none') {
        return selectAllCheckbox.checked = false;
    }
    return selectAllCheckbox.indeterminate = true;
}

function setCheckboxCheckedStatesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked) {
    return getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`li:not(.filter-no-match, .search-no-match) input[type="checkbox"]`).forEach(checkbox => {
        checkbox.checked = isEachFilteredCheckboxChecked;
    });
}

function checkAllCheckboxesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked) {
    setCheckboxCheckedStatesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked);
    // <details> open states are only toggled when selecting all checkboxes
    if (isEachFilteredCheckboxChecked) setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked);
}

function setDetailNodeOpenStatesForLiNodes(liNodes, open) {
    liNodes.forEach(liNode => {
        liNode.querySelector("details").open = open;
    });
}

function setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isEachFilteredDetailsNodeOpen) {
    return getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`li:not(.filter-no-match, .search-no-match) details`).forEach(detailsNode => {
        detailsNode.open = isEachFilteredDetailsNodeOpen;
    });
}

function setExpandedStateForTreeContainerId(treeContainerId, isExpanded) {
    setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isExpanded);
}

// Search form setup

function setupInputsForTreeContainerId(treeContainerId) {
    // Enabled checkbox count hint setup
    const allCheckboxes = getCheckboxesForTreeContainerId(treeContainerId);
    const selectAllCheckboxLabel = getSelectAllCheckboxLabelForTreeContainerId(treeContainerId);
    selectAllCheckboxLabel.innerHTML += ` <span class="text-secondary">${allCheckboxes.length}</span>`;

    const topLevelDetailsNodes = document.querySelectorAll(`#${treeContainerId} .tree > li > details`);
    topLevelDetailsNodes.forEach(detailsNode => {
        const enabledCheckboxes = Array.from(detailsNode.querySelectorAll('input[type="checkbox"]:not([disabled])'));
        if (enabledCheckboxes.length > 0) {
            const firstCheckboxLabel = detailsNode.querySelector('label');
            let span = document.createElement('span');
            span.className = 'text-secondary';
            span.innerHTML = ` ${enabledCheckboxes.length}`;
            firstCheckboxLabel.after(span);
        }
    });

    const ontologyParentNodeCheckboxesForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"][data-is-parent-node="true"]`);
    ontologyParentNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
            if (childNodeCheckboxes.length > 0) {
                updateChildNodeCheckboxesByParentNodeCheckbox(checkbox);
                setSelectAllCheckboxForTreeContainerId(treeContainerId);
            }
        });
    });

    const ontologyChildNodeCheckboxesForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:not([data-parent-node-in-ontology=""])`);
    ontologyChildNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            updateParentNodeCheckboxesByChildNodeCheckbox(checkbox);
            setSelectAllCheckboxForTreeContainerId(treeContainerId);
        });
    });
    
    const allStandaloneCheckboxes = document.querySelectorAll(`#${treeContainerId} .tree > li input[type="checkbox"]`);
    allStandaloneCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            setSelectAllCheckboxForTreeContainerId(treeContainerId);
        });
    });

    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    searchBoxForTree.addEventListener("input", event => {
        filterTreeContainerIdBySearchBoxInput(treeContainerId);
    });

    // Select/Deselect all checkbox setup
    const selectAllCheckboxForTree = getSelectAllCheckboxForTreeContainerId(treeContainerId);
    selectAllCheckboxForTree.addEventListener("change", event => {
        if (selectAllCheckboxForTree.checked) {
            checkAllCheckboxesForTreeContainerId(treeContainerId, true);
        } else {
            checkAllCheckboxesForTreeContainerId(treeContainerId, false);
        }
    });
    selectAllCheckboxForTree.checked = false;
    selectAllCheckboxForTree.disabled = false;
    
    // Button setup
    const expandAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-expand-all`);
    expandAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, true);
    });

    const collapseAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-collapse-all`);
    collapseAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, false);
    });
}

function showSelectAllCheckbox(treeContainerId) {
    const selectAllCheckboxForTree = getSelectAllCheckboxForTreeContainerId(treeContainerId);
    const selectAllCheckboxLabel = getSelectAllCheckboxLabelForTreeContainerId(treeContainerId);
    selectAllCheckboxForTree.style.opacity = 1;
    selectAllCheckboxLabel.style.opacity = 1;
}

export function addTreeContainerIdToClearInputsButton(treeContainerId, clearInputsButton) {
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
        showSelectAllCheckbox(treeContainerId);
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