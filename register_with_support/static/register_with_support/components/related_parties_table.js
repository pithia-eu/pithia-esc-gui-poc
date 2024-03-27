import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

const relatedPartiesTable = editorForm.querySelector("#table-related-parties");
const relatedPartiesTableBody = relatedPartiesTable.querySelector("tbody");
const addRelatedPartyRoleButton = document.getElementById("add-rprrow-button");

function getRelatedPartiesTableRowByChildNode(childNode) {
    const relatedPartiesTableRows = relatedPartiesTableBody.querySelectorAll("tr");
    for (const row of relatedPartiesTableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
}

function getNumRemainingRelatedPartySelectsOfRow(tableRow) {
    return tableRow.querySelectorAll("select[name='related_party']").length;
}

function getNumRemainingRelatedPartyRoles() {
    return relatedPartiesTableBody.querySelectorAll("tr").length;
}

function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
}

function removeRelatedParty(event) {
    const removeRelatedPartyButton = event.currentTarget;
    const containingTableRow = getRelatedPartiesTableRowByChildNode(removeRelatedPartyButton);
    const relatedPartiesListElement = containingTableRow.querySelector("ul");
    const relatedPartyLiElements = relatedPartiesListElement.querySelectorAll("li");
    for (const liElement of relatedPartyLiElements) {
        if (liElement.contains(removeRelatedPartyButton)) {
            relatedPartiesListElement.removeChild(liElement);
            break;
        }
    }
    const remainingRelatedPartySelectsInRow = getNumRemainingRelatedPartySelectsOfRow(containingTableRow);
    if (remainingRelatedPartySelectsInRow === 1) {
        containingTableRow.querySelector(".td-related-parties .remove-rp-button").disabled = true;
    }
}

function setupRemoveRelatedPartyButton(removeRelatedPartyButton) {
    removeRelatedPartyButton.addEventListener("click", removeRelatedParty);
}

function addRelatedParty(event) {
    // Create a new related party input by
    // copying the first one in the list.
    const addRelatedPartyButton = event.currentTarget;
    const containingTableRow = getRelatedPartiesTableRowByChildNode(addRelatedPartyButton);
    const relatedPartiesListElement = containingTableRow.querySelector("ul");
    const firstRelatedPartyLiElement = relatedPartiesListElement.querySelector("li");
    const newRelatedPartyLiElement = document.createElement("li");
    newRelatedPartyLiElement.classList = firstRelatedPartyLiElement.classList;
    newRelatedPartyLiElement.innerHTML = firstRelatedPartyLiElement.innerHTML;
    
    // Update any IDs that are duplicated
    const childElementsWithIdAttribute = newRelatedPartyLiElement.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const relatedPartyLabel = containingTableRow.querySelector(`label[for="${elem.id}"]`);
        elem.id = newId;
        elem.setAttribute("aria-label", relatedPartyLabel.innerHTML);
    });

    // Enable the remove button if it's
    // disabled as there's more than one
    // related party input now.
    const removeRelatedPartyButton = newRelatedPartyLiElement.querySelector(".remove-rp-button");
    removeRelatedPartyButton.disabled = false;
    // Setup the remove button
    setupRemoveRelatedPartyButton(removeRelatedPartyButton);
    // Add the new related party input
    relatedPartiesListElement.appendChild(newRelatedPartyLiElement);
    
    // Enable the first select menu's remove
    // button if it's not already enabled.
    const remainingRelatedPartySelectsInRow = getNumRemainingRelatedPartySelectsOfRow(containingTableRow);
    if (remainingRelatedPartySelectsInRow > 1) {
        containingTableRow.querySelector(".td-related-parties .remove-rp-button").disabled = false;
    }
}

function setupAddRelatedPartyButton(addRelatedPartyButton) {
    addRelatedPartyButton.addEventListener("click", addRelatedParty);
}

function removeRelatedPartyRole(event) {
    const removeRelatedPartyRoleButton = event.currentTarget;
    const containingTableRow = getRelatedPartiesTableRowByChildNode(removeRelatedPartyRoleButton);
    relatedPartiesTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton) {
    removeRelatedPartyRoleButton.addEventListener("click", removeRelatedPartyRole);
}

function addRelatedPartyRole(event) {
    // Create new table row by copying HTML of
    // first table row.
    const relatedPartiesTableFirstRow = relatedPartiesTableBody.querySelector("tr");
    const newRow = document.createElement("TR");
    newRow.innerHTML = relatedPartiesTableFirstRow.innerHTML;
    
    // Reset any child elements to their default
    // states if not already.
    const newRowRelatedPartiesList = newRow.querySelector("td.td-related-parties ul");
    if (newRowRelatedPartiesList.querySelectorAll("li").length > 0) {
        newRowRelatedPartiesList.innerHTML = newRowRelatedPartiesList.querySelector("li").outerHTML;
    }
    const newRowHighlightedInputs = newRow.querySelectorAll("input.was-validated");
    newRowHighlightedInputs.forEach(input => {
        input.classList.remove("was-validated");
        input.classList.remove("is-invalid");
    });

    // Ensure the IDs of any child elements are
    // unique.
    const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const correspondingLabels = newRow.querySelectorAll(`label[for="${elem.id}"]`);
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
    });
    
    // Set up each of the buttons in the row
    const addRelatedPartyButton = newRow.querySelector(".add-rp-button");
    setupAddRelatedPartyButton(addRelatedPartyButton);
    const removeRelatedPartyButton = newRow.querySelector(".remove-rp-button");
    setupRemoveRelatedPartyButton(removeRelatedPartyButton);
    const removeRelatedPartyRoleButton = newRow.querySelector(".remove-rprrow-button");
    removeRelatedPartyRoleButton.disabled = false;
    setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton);

    // Add the row to the table
    relatedPartiesTableBody.appendChild(newRow);

    // Enable the first row's remove button if
    // it's not already enabled.
    const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
    if (numRemainingTableRows > 1) {
        const firstRemoveRoleButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
        firstRemoveRoleButton.disabled = false;
    }
}

function setupAddRelatedPartyRoleButton() {
    addRelatedPartyRoleButton.addEventListener("click", addRelatedPartyRole);
}

export function setupRelatedPartiesTable() {
    const relatedPartiesTableRows = relatedPartiesTableBody.querySelectorAll("tr");
    relatedPartiesTableRows.forEach(row => {
        const addRelatedPartyButton = row.querySelector(".add-rp-button");
        setupAddRelatedPartyButton(addRelatedPartyButton);
        const removeRelatedPartyButton = row.querySelector(".remove-rp-button");
        setupRemoveRelatedPartyButton(removeRelatedPartyButton);
        if (getNumRemainingRelatedPartySelectsOfRow(row) === 1) {
            removeRelatedPartyButton.disabled = true;
        }
        const removeRelatedPartyRoleButton = document.querySelector(".remove-rprrow-button");
        setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton);
        if (relatedPartiesTableRows.length === 1) {
            removeRelatedPartyRoleButton.disabled = true;
        }
    });
    setupAddRelatedPartyRoleButton();
}