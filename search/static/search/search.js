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
    if (!parentNodeCheckbox) {
        return;
    }
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
    });
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



// Keyword search

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

function getSearchBoxInputFilterResultsForTreeContainerId(treeContainerId, searchBoxInput) {
    const allCheckboxLabelsForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll("label");
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace

    const validCheckboxes = [];
    let liNodesToShow = [], liNodesToHide = [];
    allCheckboxLabelsForTree.forEach(label => {
        // All keywords should be present
        // in a label (AND match).
        let matchCountForLabel = 0;
        searchBoxInputSplit.forEach(inputTerm => {
            if (label.innerHTML.toLowerCase().includes(inputTerm.toLowerCase())) {
                matchCountForLabel++;
            }
        });

        const enclosingLiNode = getEnclosingLiNode(label);
        // If all keywords are not present in the
        // label, add its <li> to an array of <li>s
        // to be hidden.
        if (matchCountForLabel !== searchBoxInputSplit.length) {
            return liNodesToHide.push(enclosingLiNode);
        }

        // If all keywords are present, increase the
        // total match count, and add the enclosing
        // <li> of the label to an array of <li>s to
        // be shown.
        const checkboxForLabel = document.getElementById(label.htmlFor);
        if (!checkboxForLabel.disabled) {
            // If the checkbox the label is associated
            // with is enabled, this is counted as a
            // valid match.
            validCheckboxes.push(checkboxForLabel);
        }
        liNodesToShow.push(enclosingLiNode);

        // Find parent <li>s by finding the parent
        // checkbox of the checkbox the label is
        // associated with.
        const childNodeCheckboxes = enclosingLiNode.getElementsByTagName("input");
        if (childNodeCheckboxes.length > 0) {
            const firstChildNodeCheckbox = childNodeCheckboxes[0];
            const parentNodeCheckboxes = getParentNodeCheckboxes(firstChildNodeCheckbox);
            parentNodeCheckboxes.forEach(checkbox => {
                const enclosingLiNodeOfParentNodeCheckbox = getEnclosingLiNode(checkbox);
                liNodesToShow.push(enclosingLiNodeOfParentNodeCheckbox);
            });
        }
    });
    liNodesToHide = Array.from(new Set(liNodesToHide));
    liNodesToShow = Array.from(new Set(liNodesToShow));

    return {
        validCheckboxes: validCheckboxes,
        liNodesToHide: liNodesToHide,
        liNodesToShow: liNodesToShow,
    }
}

function applySearchBoxInputFiltersToLiNodes(liNodesToHide, liNodesToShow) {
    addSearchBoxInputFiltersToLiNodes(liNodesToHide);
    removeSearchBoxInputFiltersFromLiNodes(liNodesToShow);
}

function hideSearchBoxInputCheckboxForTreeContainerId(treeContainerId) {
    document.querySelector(`#${treeContainerId} .keyword-input-checkbox-container`).classList.add("d-none");
}

export function updateAndShowSearchBoxInputCheckboxForTreeContainerId(treeContainerId, matchCountTotal) {
    document.querySelector(`#${treeContainerId} .checkbox-num-hint-keyword-input`).innerHTML = `${matchCountTotal} keyword ${(matchCountTotal === 1) ? 'match' : 'matches'}`;
    document.querySelector(`#${treeContainerId} .keyword-input-checkbox-container`).classList.remove("d-none");
}




// Common query selectors

export function getSearchTermsContainerForTreeContainerId(treeContainerId) {
    return document.querySelector(`#${treeContainerId} .tree-search-terms`);
}

function getCheckboxesForTreeContainerId(treeContainerId) {
    return Array.from(getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:not([disabled])`));
}

function getCheckedCheckboxesForTreeContainerId(treeContainerId) {
    return Array.from(getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:checked:not([disabled])`));
}


// Select/deselect all checkbox management

export function getSelectAllCheckboxForTreeContainerId(treeContainerId) {
    return document.querySelector(`#${treeContainerId} input[type="checkbox"][id$="select-all-checkbox"]`);
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

function setSelectAllCheckboxStateForTreeContainerId(treeContainerId) {
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
    return getCheckboxesForTreeContainerId(treeContainerId).forEach(checkbox => {
        checkbox.checked = isEachFilteredCheckboxChecked;
    });
}

function checkAllVisibleCheckboxesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked) {
    setCheckboxCheckedStatesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked);
    // <details> open states are only toggled when selecting all checkboxes
    if (isEachFilteredCheckboxChecked) setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isEachFilteredCheckboxChecked);
}



// Tree expanded/collapsed management

function setDetailNodeOpenStatesForLiNodes(liNodes, open) {
    liNodes.forEach(liNode => {
        const detailsNode = liNode.querySelector("details");
        if (detailsNode) detailsNode.open = open;
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
    // const topLevelDetailsNodes = document.querySelectorAll(`#${treeContainerId} .tree > li > details`);
    // topLevelDetailsNodes.forEach(detailsNode => {
    //     const enabledCheckboxes = Array.from(detailsNode.querySelectorAll('input[type="checkbox"]:not([disabled])'));
    //     if (enabledCheckboxes.length > 0) {
    //         const firstCheckboxLabel = detailsNode.querySelector('label');
    //         let span = document.createElement('span');
    //         span.className = 'text-body-secondary';
    //         span.innerHTML = ` ${enabledCheckboxes.length}`;
    //         firstCheckboxLabel.after(span);
    //     }
    // });

    const ontologyParentNodeCheckboxesForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"][data-is-parent-node="true"]`);
    ontologyParentNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
            if (childNodeCheckboxes.length > 0) {
                updateChildNodeCheckboxesByParentNodeCheckbox(checkbox);
                setSelectAllCheckboxStateForTreeContainerId(treeContainerId);
            }
        });
    });

    const ontologyChildNodeCheckboxesForTree = getSearchTermsContainerForTreeContainerId(treeContainerId).querySelectorAll(`input[type="checkbox"]:not([data-parent-node-in-ontology=""])`);
    ontologyChildNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            updateParentNodeCheckboxesByChildNodeCheckbox(checkbox);
            setSelectAllCheckboxStateForTreeContainerId(treeContainerId);
        });
    });
    
    const allStandaloneCheckboxes = document.querySelectorAll(`#${treeContainerId} .tree > li input[type="checkbox"]`);
    allStandaloneCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            setSelectAllCheckboxStateForTreeContainerId(treeContainerId);
        });
    });
    
    // Button setup
    const expandAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-expand-all`);
    expandAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, true);
    });

    const collapseAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-collapse-all`);
    collapseAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, false);
    });

    // Select/Deselect all checkbox setup
    // Enabled checkbox count hint setup
    const enabledCheckboxes = getCheckboxesForTreeContainerId(treeContainerId);
    document.querySelector(`#${treeContainerId} .checkbox-num-hint-all`).innerHTML = enabledCheckboxes.length;

    const selectAllCheckboxForTree = getSelectAllCheckboxForTreeContainerId(treeContainerId);
    selectAllCheckboxForTree.checked = false;
    selectAllCheckboxForTree.addEventListener("change", event => {
        if (selectAllCheckboxForTree.checked) {
            checkAllVisibleCheckboxesForTreeContainerId(treeContainerId, true);
        } else {
            checkAllVisibleCheckboxesForTreeContainerId(treeContainerId, false);
        }
    });

    // Keyword search setup
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxCheckbox = document.querySelector(`#${treeContainerId} input[type="checkbox"][id$="keyword-input-checkbox"]`);
    let checkboxesMatchingSearch = [];

    searchBoxForTree.addEventListener("input", event => {
        const searchBoxInput = searchBoxForTree.value;
        if (searchBoxInput === "") {
            // Remove search box filters if input is
            // blank.
            const hiddenLisForTreeContainer = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId);
            removeSearchBoxInputFiltersFromLiNodes(hiddenLisForTreeContainer);
            hideSearchBoxInputCheckboxForTreeContainerId(treeContainerId)
            selectAllCheckboxForTree.disabled = false;
            expandAllButtonForTree.disabled = false;
            collapseAllButtonForTree.disabled = false;
            return;
        }
        const filterResults = getSearchBoxInputFilterResultsForTreeContainerId(treeContainerId, searchBoxInput);

        // Reset search box checkbox and its variables
        const allCheckedCheckboxes = getCheckedCheckboxesForTreeContainerId(treeContainerId);
        checkboxesMatchingSearch = filterResults.validCheckboxes;
        searchBoxCheckbox.checked = checkboxesMatchingSearch.every(c => allCheckedCheckboxes.includes(c));
        
        // Disable select all checkbox
        selectAllCheckboxForTree.disabled = true;
        expandAllButtonForTree.disabled = true;
        collapseAllButtonForTree.disabled = true;

        // Filter by search box input
        applySearchBoxInputFiltersToLiNodes(filterResults.liNodesToHide, filterResults.liNodesToShow);


        // Collapse hidden nodes, expand visible ones
        setDetailNodeOpenStatesForLiNodes(filterResults.liNodesToHide, false);
        setDetailNodeOpenStatesForLiNodes(filterResults.liNodesToShow, true);

        // Update numbers and show checkbox for search box input
        if (checkboxesMatchingSearch.length > 0) {
            return updateAndShowSearchBoxInputCheckboxForTreeContainerId(treeContainerId, checkboxesMatchingSearch.length);
        }
        return hideSearchBoxInputCheckboxForTreeContainerId(treeContainerId);
    });
    
    searchBoxCheckbox.addEventListener("change", event => {
        checkboxesMatchingSearch.forEach(checkbox => {
            checkbox.checked = searchBoxCheckbox.checked;
            updateChildNodeCheckboxesByParentNodeCheckbox(checkbox);
            updateParentNodeCheckboxesByChildNodeCheckbox(checkbox);
        });
        setSelectAllCheckboxStateForTreeContainerId(treeContainerId);
    });
}

export function addTreeContainerIdToClearInputsButton(treeContainerId, clearInputsButton) {
    clearInputsButton.addEventListener("click", event => {
        checkAllVisibleCheckboxesForTreeContainerId(treeContainerId, false);
        const checkboxFilteredLiNodesForTreeContainerId = getLiNodesHiddenByCheckboxFilterForTreeContainerId(treeContainerId);
        removeCheckboxFiltersFromLiNodes(checkboxFilteredLiNodesForTreeContainerId);
        setSelectAllCheckboxStateForTreeContainerId(treeContainerId);
    });
}

export async function setupSearchFormComponent(html, treeContainerId, callback) {
    setTimeout(async () => {
        document.querySelector(`#${treeContainerId} .tree-search-terms`).innerHTML = html;
        setupInputsForTreeContainerId(treeContainerId);
        document.querySelector(`#${treeContainerId} .select-all-checkboxes-container`).classList.remove("d-none");
        document.querySelector(`#${treeContainerId} .select-all-checkbox-container`).classList.remove("opacity-0");
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

document.getElementById("ontology-search-form").addEventListener("submit", event => {
    const checkedCheckboxes = document.querySelectorAll("#ontology-search-form input[type=checkbox].search-term-checkbox:checked:not(:disabled, [name=phenomenon], [name=measurand])");
    if (checkedCheckboxes.length === 0) {
        event.preventDefault();
        return alert('Select at least one Feature of Interest, Computation Type, Instrument Type, Annotation Type or Observed Property.');
    }
});