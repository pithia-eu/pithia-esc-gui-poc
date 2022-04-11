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
    const searchBoxInputSplit = searchBoxInput.split("/\s+/"); // /\s+/ regex means to split by any length of whitespace

    if (searchBoxInput === "") {
        const allHiddenLisForTree = document.querySelectorAll(`#${treeContainerId} li`);
        allHiddenLisForTree.forEach(li => {
            li.classList.remove("search-no-match");
        });
    } else {
        allCheckboxLabelsForTree.forEach(label => {
            const enclosingLiNode = getEnclosingLiNode(label);
            let inputMatchFound = false;
            searchBoxInputSplit.forEach(inputTerm => {
                if (label.innerHTML.toLowerCase().includes(inputTerm.toLowerCase())) {
                    inputMatchFound = true;
                }
            });
            if (inputMatchFound) {
                enclosingLiNode.classList.remove("search-no-match");
            } else {
                enclosingLiNode.classList.add("search-no-match");
            }
        });
    }
}

function setupCheckboxesForTreeContainer(treeContainerId) {
    const ontologyParentNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"][data-is-parent-node="true"]`);
    const ontologyChildNodeCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]:not([data-parent-node-in-ontology=""])`);
    const searchBoxForTree = document.querySelector(`#${treeContainerId} .tree-search-box`);

    ontologyParentNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
            if (childNodeCheckboxes.length > 0) {
                updateChildNodeCheckboxes(checkbox);
            }
        });
    });

    ontologyChildNodeCheckboxesForTree.forEach(checkbox => {
        checkbox.addEventListener("change", event => {
            updateParentNodeCheckboxes(checkbox);
        });
    });

    if (treeContainerId !== "observed-properties-tree-search-container") {
        const allCheckboxesForTree = document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]`);
        allCheckboxesForTree.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                filterObservedPropertyCheckboxes(treeContainerId, document.querySelectorAll(`#${treeContainerId} input[type="checkbox"]:checked`));
            });
        });
    }

    searchBoxForTree.addEventListener("input", event => {
        filterTermsFromSearchBoxInput(treeContainerId);
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
        setupCheckboxesForTreeContainer(treeContainerId);
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
});