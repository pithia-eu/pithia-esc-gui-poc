function getEnclosingLiNode(elem) {
    let currentParentNode = elem;
    let currentChildNode = elem;
    while (currentParentNode !== null && currentParentNode.nodeName !== "LI") {
        currentParentNode = currentChildNode.parentNode;
        currentChildNode = currentParentNode;
    }
    return currentParentNode;
}

function updateParentNodeCheckboxes(childNodeCheckbox) {
    const siblingNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${childNodeCheckbox.dataset.parentNodeInOntology}']`);
    const siblingNodeCheckboxesChecked = document.querySelectorAll(`input[data-parent-node-in-ontology='${childNodeCheckbox.dataset.parentNodeInOntology}']:checked`);
    const parentNodeCheckbox = document.getElementById(childNodeCheckbox.dataset.parentNodeInOntology);
    parentNodeCheckbox.checked = siblingNodeCheckboxes.length === siblingNodeCheckboxesChecked.length;
    if (parentNodeCheckbox.dataset.parentNodeInOntology !== "") {
        updateParentNodeCheckboxes(parentNodeCheckbox);
    }
}

function updateChildNodeCheckboxes(parentNodeCheckbox) {
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
            updateChildNodeCheckboxes(checkbox);
        }
    })
}

function filterObservedPropertyCheckboxes(treeContainerId, selectedCheckboxes) {
    const observedPropertyCheckboxes = document.querySelectorAll(`#observed-properties-tree-search-container input[type="checkbox"]`);
    let vocabFilter = "";
    if (selectedCheckboxes.length === 0) {
        const hiddenObservedPropertyLis = document.querySelectorAll(`#observed-properties-tree-search-container li`);
        hiddenObservedPropertyLis.forEach(li => {
            li.classList.remove("filter-no-match");
        });
    } else {
        switch (treeContainerId) {
            case "measurands-tree-search-container":
                vocabFilter = "measurands";
                break;
            case "qualifiers-tree-search-container":
                vocabFilter = "qualifiers";
                break;
            default:
                vocabFilter = "phenomenons";
        }
        observedPropertyCheckboxes.forEach(opCheckbox => {
            let isOpCheckboxAndChildrenVisible = false;
            // OR match
            selectedCheckboxes.forEach(checkbox => {
                if (opCheckbox.dataset && opCheckbox.dataset[vocabFilter] && opCheckbox.dataset[vocabFilter].includes(checkbox.id)) {
                    isOpCheckboxAndChildrenVisible = true;
                }
            });
            const enclosingLiNode = getEnclosingLiNode(opCheckbox);
            if (isOpCheckboxAndChildrenVisible) {
                enclosingLiNode.classList.remove("filter-no-match");
            } else {
                enclosingLiNode.classList.add("filter-no-match");
            }
        });
    }
}

function filterTermsFromSearchBoxInput(treeContainerId) {
    const allCheckboxLabelsForTree = document.querySelectorAll(`#${treeContainerId} .tree-search-terms label`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    const searchBoxInput = searchBoxForTree.value;
    const searchBoxInputSplit = searchBoxInput.split(/\s+/).filter(string => string !== ""); // /\s+/ regex means to split by any length of whitespace
    
    if (searchBoxInput === "") {
        const allHiddenLisForTree = document.querySelectorAll(`#${treeContainerId} li`);
        allHiddenLisForTree.forEach(li => {
            li.classList.remove("search-no-match");
        });
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
        hiddenLiNodes.forEach(li => {
            li.classList.add("search-no-match");
        });
        visibleLiNodes.forEach(li => {
            li.classList.remove("search-no-match");
        });
    }
}

function setupInputsForTreeContainer(treeContainerId) {
    const ontologyParentNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"][data-is-parent-node="true"]`);
    ontologyParentNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
            if (childNodeCheckboxes.length > 0) {
                updateChildNodeCheckboxes(checkbox);
            }
        });
    });

    const ontologyChildNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]:not([data-parent-node-in-ontology=""])`);
    ontologyChildNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            updateParentNodeCheckboxes(checkbox);
        });
    });

    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);
    searchBoxForTree.addEventListener("input", event => {
        filterTermsFromSearchBoxInput(treeContainerId);
    });

    const allCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`);
    if (treeContainerId !== "observed-properties-tree-search-container") {
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                filterObservedPropertyCheckboxes(treeContainerId, document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]:checked`));
            });
        });
    }

    const detailsElemsForTree = document.querySelectorAll(`#${treeContainerId} details`);
    const deselectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-deselect-all`);
    deselectAllButtonForTree.addEventListener("click", event => {
        searchBoxForTree.value = "";
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.checked = false;
        });
        detailsElemsForTree.forEach(details => {
            details.open = false;
        });
    });

    const selectAllButtonForTree = document.querySelector(`#${treeContainerId} .btn-select-all`);
    selectAllButtonForTree.addEventListener("click", event => {
        searchBoxForTree.value = "";
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.checked = true;
        });
        detailsElemsForTree.forEach(details => {
            details.open = true;
        });
    });
}

async function parseResponseText(response) {
    return response.text();
}

function getTreeContainerIdFromHTML(html) {
    if (html.includes('name="measurands"')) {
        return "measurands-tree-search-container";
    } else if (html.includes('name="observed_properties"')) {
        return "observed-properties-tree-search-container";
    } else if (html.includes('name="phenomenons"')) {
        return "phenomenons-tree-search-container";
    } else if (html.includes('name="qualifiers"')) {
        return "qualifiers-tree-search-container";
    }
    return "unknown";
}

async function loadSearchFormComponent(html) {
    let treeContainerId = getTreeContainerIdFromHTML(html);
    if (treeContainerId === "unknown") {
        return;
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
        // Clear all search boxes, checkboxes, unhide all LI elements, etc.
        const allTreeContainerSearchBoxes = document.querySelectorAll(".tree-search-box");
        allTreeContainerSearchBoxes.forEach(searchBox => {
            searchBox.value = "";
        })

        const allTreeContainerCheckboxes = document.querySelectorAll(".tree-search-terms input[type='checkbox']");
        allTreeContainerCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        const allTreeContainerLis = document.querySelectorAll(".tree-search-terms li");
        allTreeContainerLis.forEach(li => {
            li.classList.remove("filter-no-match");
            li.classList.remove("search-no-match");
        });

        const allTreeDetailsElems = document.querySelectorAll(".tree-search-terms details");
        allTreeDetailsElems.forEach(details => {
            details.open = false;
        });
    });
});