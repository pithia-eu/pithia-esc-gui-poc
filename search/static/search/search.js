const ontologyTreeLiElems = document.querySelectorAll("li");
const ontologyTreeCheckboxesL1 = document.querySelectorAll("input[data-list-level='1']");
function updateParentCheckboxes(nodeId) {
    
}

function updateChildCheckboxes(nodeId) {
    const parentNodeCheckbox = document.getElementById(nodeId);
    const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-tree='${nodeId}']`);
    childNodeCheckboxes.forEach(checkbox => {
        checkbox.checked = parentNodeCheckbox.checked;
        const childNodeCheckboxesOfChildNodeCheckbox = document.querySelectorAll(`input[data-parent-node-in-tree='${checkbox.id}']`);
        if (childNodeCheckboxesOfChildNodeCheckbox.length > 0) {
            updateChildCheckboxes(checkbox.id);
        }
    })
}

ontologyTreeCheckboxesL1.forEach(checkbox => {
    checkbox.addEventListener("change", event => {
        const childNodeCheckboxes = document.querySelectorAll(`input[data-parent-node-in-tree='${checkbox.id}']`);
        if (childNodeCheckboxes.length > 0) {
            updateChildCheckboxes(checkbox.id);
        }
    });
});