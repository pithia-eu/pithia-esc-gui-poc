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

// Utils
function getRelatedPartiesTableRowByChildNode(childNode) {
    const relatedPartiesTableRows = relatedPartiesTableBody.querySelectorAll("tr");
    for (const row of relatedPartiesTableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
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

function resetDuplicatedRowElements(newRow) {
    // Remove any validation styling if there
    // is any
    const newRowHighlightedSelects = newRow.querySelectorAll("select.was-validated");
    newRowHighlightedSelects.forEach(select => {
        select.classList.remove("was-validated");
        select.classList.remove("is-invalid");
    });

    // Reset any selected choices
    const rowSelects = newRow.querySelectorAll("select");
    rowSelects.forEach(select => {
        select.querySelectorAll("option[selected]").forEach(option => {
            option.selected = false;
        });
        select.className = "form-select";
    });

    // Remove any custom select elements
    const tsWrappers = newRow.querySelectorAll(".ts-wrapper");
    tsWrappers.forEach(tsw => {
        tsw.remove();
    });

    // Enable remove related party role button
    const removeRelatedPartyRoleButton = newRow.querySelector(".remove-rprrow-button");
    removeRelatedPartyRoleButton.disabled = false;
}

function fixDuplicatedRowElementIds(newRow) {
    const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const correspondingLabels = newRow.querySelectorAll(`label[for="${elem.id}"]`);
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
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
    resetDuplicatedRowElements(newRow);

    // Ensure the IDs of any child elements are
    // unique.
    fixDuplicatedRowElementIds(newRow);
    
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

    window.dispatchEvent(new CustomEvent("newSelectsAdded", {
        detail: Array.from(newRow.querySelectorAll("select:not([multiple])")).map(select => select.id),
    }));
    window.dispatchEvent(new CustomEvent("newMultipleChoiceSelectsAdded", {
        detail: Array.from(newRow.querySelectorAll("select[multiple]")).map(select => select.id),
    }));

    return newRow;
}

function setupSelectEventMappingForRow(tableRow) {
    const selects = Array.from(tableRow.querySelectorAll("select"));
    selects.forEach(s => {
        s.addEventListener("change", e => {
            prepareRelatedPartiesJSON();
        });
    });
}

function setupRowEventListeners(tableRow) {
    setupSelectEventMappingForRow(tableRow);
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

        // Load role
        const roleSelect = correspondingRow.querySelector("select[name='related_party_role']");
        roleSelect.value = role;
        window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
            detail: roleSelect.id,
        }));

        // Load parties
        const partySelect = correspondingRow.querySelector("select[name='related_party']");
        parties.forEach(party => {
            partySelect.querySelector(`option[value="${party}"]`).selected = true;
        });
        window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
            detail: partySelect.id,
        }));

        rowIndex += 1;
    }
}

export function setupRelatedPartiesTable() {
    const firstRelatedPartiesTableRow = relatedPartiesTableBody.querySelector("tr");
    loadPreviousData();
    setupRowEventListeners(firstRelatedPartiesTableRow);
    setupAddRelatedPartyRoleButton();
}