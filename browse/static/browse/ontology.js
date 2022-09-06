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

function setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, open) {
    return document.querySelectorAll(`#${treeContainerId} details`).forEach(detailsNode => {
        detailsNode.open = open;
    });
}

function setupInputsForTreeContainerId(treeContainerId) {
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    searchBoxForTree.addEventListener("input", event => {
        filterTreeContainerIdBySearchBoxInput(treeContainerId);
    });
}

// Search form setup

export function addTreeContainerIdToClearInputsButton(treeContainerId) {
    const clearInputsButton = document.querySelector(".btn-clear");
    clearInputsButton.addEventListener("click", event => {
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

    return fetch(`/browse/ontology/terms/${ontologyComponent}/`, fetchParams)
        .then(parseResponseText)
        .catch (error => {
            console.error(`Unable to fetch "${ontologyComponent}" terms list.`);
            console.error(error);
        });
}