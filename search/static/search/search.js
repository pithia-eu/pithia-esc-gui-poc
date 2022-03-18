function getEnclosingLiNode(checkbox) {
    let currentParentNode = checkbox;
    let currentChildNode = checkbox;
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

async function loadSearchFormComponents() {
    const fetchParams = { method: "GET" };
    const measurandsResponse = fetch("/search/measurand/", fetchParams);
    const observedPropertiesResponse = fetch("/search/observedProperty/", fetchParams);
    const phenomenonsResponse = fetch("/search/phenomenon/", fetchParams);
    const qualifiersResponse = fetch("/search/qualifier/", fetchParams);
    const responses = await Promise.all([
        measurandsResponse,
        observedPropertiesResponse,
        phenomenonsResponse,
        qualifiersResponse,
    ]);
    
    setTimeout(async () => {
        const responsesParsed = await Promise.all(responses.map(response => response.text()));
        const measurandsFormComponent = responsesParsed[0];
        const observedPropertiesFormComponent = responsesParsed[1];
        const phenomenonsFormComponent = responsesParsed[2];
        const qualifiersFormComponent = responsesParsed[3];
        document.getElementById("measurands-tree-container").innerHTML = measurandsFormComponent;
        document.getElementById("observed-properties-tree-container").innerHTML = observedPropertiesFormComponent;
        document.getElementById("phenomenons-tree-container").innerHTML = phenomenonsFormComponent;
        document.getElementById("qualifiers-tree-container").innerHTML = qualifiersFormComponent;
        treeContainers.forEach(tc => {
            tc.style.opacity = 1;
        });
        const ontologyParentNodeCheckboxes = document.querySelectorAll(".tree input[data-is-parent-node='true']");
        const ontologyChildNodeCheckboxes = document.querySelectorAll(".tree input:not([data-parent-node-in-ontology=''])");
    
        ontologyParentNodeCheckboxes.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-ontology='${checkbox.id}']`);
                if (childNodeCheckboxes.length > 0) {
                    updateChildNodeCheckboxes(checkbox);
                }
            });
        });
    
        ontologyChildNodeCheckboxes.forEach(checkbox => {
            checkbox.addEventListener("change", event => {
                updateParentNodeCheckboxes(checkbox);
            });
        });
    }, 300);
    const treeContainers = document.querySelectorAll(".tree-container");
    treeContainers.forEach(tc => {
        tc.style.opacity = 0;
    });
}

document.getElementById("search-script").addEventListener("load", async event => {
    await loadSearchFormComponents();
});