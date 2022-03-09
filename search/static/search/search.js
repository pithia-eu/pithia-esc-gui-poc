const ontologyParentNodeCheckboxes = document.querySelectorAll(".tree input[data-is-parent-node='true']");
const ontologyChildNodeCheckboxes = document.querySelectorAll(".tree input:not([data-parent-node-in-ontology=''])");


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