import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareRelatedPartiesJSON,
} from "/static/register_with_support/components/json_field_processing.js";

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

function removeRelatedParty(liChildElement) {
    const containingTableRow = getRelatedPartiesTableRowByChildNode(liChildElement);
    const relatedPartiesListElement = containingTableRow.querySelector("ul");
    const relatedPartyLiElements = relatedPartiesListElement.querySelectorAll("li");
    for (const liElement of relatedPartyLiElements) {
        if (liElement.contains(liChildElement)) {
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
    removeRelatedPartyButton.addEventListener("click", e => {
        removeRelatedParty(e.currentTarget);
        prepareRelatedPartiesJSON();
    });
}

function addRelatedParty(rowChildElement) {
    // Create a new related party input by
    // copying the first one in the list.
    const containingTableRow = getRelatedPartiesTableRowByChildNode(rowChildElement);
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
    return newRelatedPartyLiElement;
}

function setupAddRelatedPartyButton(addRelatedPartyButton) {
    addRelatedPartyButton.addEventListener("click", e => {
        addRelatedParty(e.currentTarget);
        prepareRelatedPartiesJSON();
    });
}

function removeRelatedPartyRole(rowChildElement) {
    const containingTableRow = getRelatedPartiesTableRowByChildNode(rowChildElement);
    relatedPartiesTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton) {
    removeRelatedPartyRoleButton.addEventListener("click", e => {
        removeRelatedPartyRole(e.currentTarget);
        prepareRelatedPartiesJSON();
    });
}

function addRelatedPartyRole() {
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
    const rowSelects = newRow.querySelectorAll("select");
    rowSelects.forEach(select => {
        select.value = "";
    });
    const removeRelatedPartyButton = newRow.querySelector(".remove-rp-button");
    removeRelatedPartyButton.disabled = true;
    const removeRelatedPartyRoleButton = newRow.querySelector(".remove-rprrow-button");
    removeRelatedPartyRoleButton.disabled = false;

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
    
    // Set up the row's event listeners
    setupRowEventListeners(newRow);

    // Add the row to the table
    relatedPartiesTableBody.appendChild(newRow);

    // Enable the first row's remove button if
    // it's not already enabled.
    const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
    if (numRemainingTableRows > 1) {
        const firstRemoveRoleButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
        firstRemoveRoleButton.disabled = false;
    }

    return newRow;
}

function setupSelectEventMappingForRow(tableRow) {
    const selects = tableRow.querySelectorAll("select");
    selects.forEach(input => {
        input.addEventListener("change", () => {
            prepareRelatedPartiesJSON();
        });
    });
}

function setupRowEventListeners(tableRow) {
    setupSelectEventMappingForRow(tableRow);
    const addRelatedPartyButton = tableRow.querySelector(".add-rp-button");
    setupAddRelatedPartyButton(addRelatedPartyButton);
    const removeRelatedPartyButton = tableRow.querySelector(".remove-rp-button");
    setupRemoveRelatedPartyButton(removeRelatedPartyButton);
    const removeRelatedPartyRoleButton = tableRow.querySelector(".remove-rprrow-button");
    setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton);
}

function setupAddRelatedPartyRoleButton() {
    addRelatedPartyRoleButton.addEventListener("click", () => {
        addRelatedPartyRole();
        prepareRelatedPartiesJSON();
    });
}

function loadPreviousData() {
    const previousData = JSON.parse(editorForm.querySelector("input[name='related_parties_json']").value);
    if (!previousData) {
        return;
    }
    for (let i = 0; i < previousData.length - 1; i++) {
        addRelatedPartyRole();
    }
    let rowIndex = 1;
    for (const relatedPartyObject of previousData) {
        const role = relatedPartyObject.role;
        const parties = relatedPartyObject.parties;
        const correspondingRow = relatedPartiesTableBody.querySelector(`tr:nth-of-type(${rowIndex})`);
        // Role
        const roleSelect = correspondingRow.querySelector("select[name='related_party_role']");
        roleSelect.value = role;
        // Parties
        const partySelect = correspondingRow.querySelector("select[name='related_party']");
        partySelect.value = parties[0];
        if (parties.length > 1) {
            for (let i = 1; i < parties.length; i++) {
                const newPartyLiElement = addRelatedParty(partySelect);
                const correspondingPartySelect = newPartyLiElement.querySelector("select[name='related_party']");
                correspondingPartySelect.value = parties[i];
            }
        }
        rowIndex += 1;
    }
}

export function setupRelatedPartiesTable() {
    const firstRelatedPartiesTableRow = relatedPartiesTableBody.querySelector("tr");
    loadPreviousData();
    setupRowEventListeners(firstRelatedPartiesTableRow);
    setupAddRelatedPartyRoleButton();
}