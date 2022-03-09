const ontologyParentNodeCheckboxes = document.querySelectorAll("input[data-is-parent-node='true']");
const ontologyChildNodeCheckboxes = document.querySelectorAll("input:not([data-parent-node-in-ontology=''])");


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