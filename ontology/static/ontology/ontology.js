import {
    setupOntologyIriCopyButtons,
} from "/static/ontology/ontology_utils_setup.js";

const SEARCH_BOX_INPUT_FILTER_CLASS = "search-no-match";
const noSearchMatchesFound = document.getElementById("no-search-results-msg");
const numberOfVisibleTermsElement = document.querySelector("#number-of-terms");


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

export function getParentNodeElems(div, parentNodeElems) {
    if (!parentNodeElems) {
        parentNodeElems = [];
    }
    if (div.dataset.parentNodeInOntology === "") {
        return parentNodeElems;
    }
    const parentNodeElem = document.getElementById(div.dataset.parentNodeInOntology);
    parentNodeElems.push(parentNodeElem);
    if (parentNodeElem.dataset.parentNodeInOntology !== "") {
        parentNodeElems = getParentNodeElems(parentNodeElem, parentNodeElems);
    }
    return parentNodeElems;
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
    const keywordSearchableElems = document.querySelectorAll(`#${treeContainerId} .tree-search-terms .keyword-searchable`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxInput = searchBoxForTree.value;
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace
    
    if (searchBoxInput === "") {
        const hiddenLisForTreeContainer = getLiNodesHiddenBySearchBoxInputFilterForTreeContainerId(treeContainerId);
        removeSearchBoxInputFiltersFromLiNodes(hiddenLisForTreeContainer);
        setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, false);
        return numberOfVisibleTermsElement.textContent = document.querySelectorAll(`#${treeContainerId} .tree-search-terms .ontology-term`).length;
    }

    let liNodesToShow = [], liNodesToHide = [];
    keywordSearchableElems.forEach(elem => {
        // AND match
        let numInputMatchesFound = 0;
        searchBoxInputSplit.forEach(inputTerm => {
            if (!elem.textContent.toLowerCase().includes(inputTerm.toLowerCase())) {
                return;
            }
            numInputMatchesFound++;
        });

        const enclosingLiNode = getEnclosingLiNode(elem);
        if (numInputMatchesFound !== searchBoxInputSplit.length) {
            return liNodesToHide.push(enclosingLiNode);
        }
        liNodesToShow.push(enclosingLiNode);
        const childNodeDivs = enclosingLiNode.getElementsByTagName("div");
        if (childNodeDivs.length === 0) {
            return;
        }
        const firstChildNodeDiv = childNodeDivs[0];
        const parentNodeElems = getParentNodeElems(firstChildNodeDiv);
        parentNodeElems.forEach(div => {
            const enclosingLiNodeOfParentNodeCheckbox = getEnclosingLiNode(div);
            liNodesToShow.push(enclosingLiNodeOfParentNodeCheckbox);
        });
    });
    liNodesToHide = Array.from(new Set(liNodesToHide));
    liNodesToShow = Array.from(new Set(liNodesToShow));
    addSearchBoxInputFiltersToLiNodes(liNodesToHide);
    removeSearchBoxInputFiltersFromLiNodes(liNodesToShow);
    liNodesToShow.forEach(liNode => {
        const detailsNodes = liNode.querySelectorAll("details");
        detailsNodes.forEach(detailsNode => {
            detailsNode.open = true;
        });
    });
    noSearchMatchesFound.classList.add("d-none");
    if (liNodesToShow.length === 0) {
        noSearchMatchesFound.classList.remove("d-none");
        noSearchMatchesFound.querySelector("span").textContent = searchBoxInput;
    }
    // Update number of terms still visible
    return numberOfVisibleTermsElement.textContent = liNodesToShow.length;
}

function setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isEachFilteredDetailsNodeOpen) {
    return document.querySelector(`#${treeContainerId} .tree-search-terms`).querySelectorAll(`li:not(.search-no-match) details`).forEach(detailsNode => {
        detailsNode.open = isEachFilteredDetailsNodeOpen;
    });
}

function setExpandedStateForTreeContainerId(treeContainerId, isExpanded) {
    setDetailsNodeOpenStatesForTreeContainerId(treeContainerId, isExpanded);
}

function setupInputsForTreeContainerId(treeContainerId) {
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);

    // Keyword search setup
    searchBoxForTree.addEventListener("input", event => {
        filterTreeContainerIdBySearchBoxInput(treeContainerId);
    });

    // Expand/collapse all buttons setup
    const expandAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-expand-all`);
    expandAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, true);
    });

    const collapseAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-collapse-all`);
    collapseAllButtonForTree.addEventListener("click", event => {
        setExpandedStateForTreeContainerId(treeContainerId, false);
    });
}

// Search form setup

export async function setupSearchFormComponent(html, treeContainerId, callback) {
    setTimeout(async () => {
        document.querySelector(`#${treeContainerId} .tree-search-terms`).innerHTML = html;
        setupInputsForTreeContainerId(treeContainerId);
        await setupOntologyIriCopyButtons();
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

async function fetchTermsListForOntologyCategory() {
    const categoryListUrl = JSON.parse(document.querySelector("#category-list-url").textContent);
    const fetchParams = { method: "GET" };

    return fetch(categoryListUrl, fetchParams)
        .then(parseResponseText)
        .catch (error => {
            console.error(`Unable to fetch "${ontologyComponent}" terms list.`);
            console.error(error);
        });
}

document.getElementById("ontology-script").addEventListener("load", async event => {
    const category = JSON.parse(document.querySelector("#category").textContent);
    const termsList = await fetchTermsListForOntologyCategory();
    await setupSearchFormComponent(
        termsList,
        `${category}-tree-search-container`,
        () => {
            numberOfVisibleTermsElement.textContent = document.querySelectorAll(`#${category}-tree-search-container .tree-search-terms .ontology-term`).length;
            window.dispatchEvent(new CustomEvent("contentLoadedAsynchronously"));
        }
    );
});
