import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareStandardIdentifiersJSON,
} from "/static/register_with_support/components/json_field_processing.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
import {
    generateUniqueElemIdFromCurrentElemId,
    getNumRemainingRowsInTable,
    getTableRowByChildNode,
} from "/static/register_with_support/components/table_utils.js"

const standardIdentifiersTable = editorForm.querySelector("#table-standard-identifiers");
const standardIdentifiersTableBody = standardIdentifiersTable.querySelector("tbody");
const addStandardIdentifierRowButton = document.getElementById("add-sirow-button");
const standardIdentifiersTableRowContentTemplate = JSON.parse(document.getElementById("standard-identifier-row-content-template").textContent);


// Table management functions
function removeStandardIdentifierRow(rowChildElement) {
    const containingTableRow = getTableRowByChildNode(standardIdentifiersTableBody, rowChildElement);
    standardIdentifiersTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingRowsInTable(standardIdentifiersTableBody);
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = standardIdentifiersTableBody.querySelector(".remove-sirow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveStandardIdentifierRowButton(removeStandardIdentifierRowButton) {
    removeStandardIdentifierRowButton.addEventListener("click", e => {
        removeStandardIdentifierRow(e.currentTarget);
        prepareStandardIdentifiersJSON();
    });
}

function setupDuplicatedStandardIdentifierRow(newRow) {
    const removeStandardIdentifierRowButton = newRow.querySelector(".remove-sirow-button");
    removeStandardIdentifierRowButton.disabled = false;

    // Ensure the IDs of any child elements are
    // unique.
    const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const correspondingLabels = newRow.querySelectorAll(`label[for="${elem.id}"]`);
        const correspondingAriaDescBys = newRow.querySelectorAll(`[aria-describedby="${elem.id}"]`);
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
        correspondingAriaDescBys.forEach(elem => {
            elem.setAttribute("aria-describedby", newId);
        });
    });
}

function addStandardIdentifierRow() {
    // Create a new table row using the template
    // HTML
    const newRow = document.createElement("TR");
    newRow.innerHTML = standardIdentifiersTableRowContentTemplate;

    // Reset any unique values which may have been
    // duplicated
    setupDuplicatedStandardIdentifierRow(newRow);

    // Setup each of the row's event listeners
    setupRowEventListeners(newRow);

    // Add the row to the table
    standardIdentifiersTableBody.appendChild(newRow);

    // Enable the first row's remove button
    // if it is not already enabled.
    const numRemainingTableRows = getNumRemainingRowsInTable(standardIdentifiersTableBody);
    if (numRemainingTableRows > 1) {
        const firstRemoveRowButton = standardIdentifiersTableBody.querySelector(".remove-sirow-button");
        firstRemoveRowButton.disabled = false;
    }

    return newRow;
}

function setupAddStandardIdentifierRowButton() {
    addStandardIdentifierRowButton.addEventListener("click", () => {
        addStandardIdentifierRow();
        prepareStandardIdentifiersJSON();
    });
}

function setupInputEventMappingForRow(tableRow) {
    const inputs = Array.from(tableRow.querySelectorAll("input[name='standard_identifier_authority'], input[name='standard_identifier']"));
    inputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(inputs, inputs);
            prepareStandardIdentifiersJSON();
        });
    });
}

function setupRowEventListeners(tableRow) {
    setupInputEventMappingForRow(tableRow);
    const removeStandardIdentifierRowButton = tableRow.querySelector(".remove-sirow-button");
    setupRemoveStandardIdentifierRowButton(removeStandardIdentifierRowButton);
}

function loadPreviousData() {
    const previousData = JSON.parse(editorForm.querySelector("input[name='standard_identifiers_json']").value);
    if (!previousData) {
        return;
    }
    for (let i = 0; i < previousData.length - 1; i++) {
        addStandardIdentifierRow();
    }
    previousData.forEach((standardIdentifierObject, i) => {
        const standardIdentifierAuthority = standardIdentifierObject.authority;
        const standardIdentifier = standardIdentifierObject.value;
        const correspondingRow = standardIdentifiersTableBody.querySelector(`tr:nth-of-type(${i + 1})`);

        // Standard identifier authority
        const standardIdentifierAuthorityInput = correspondingRow.querySelector("input[name='standard_identifier_authority']");
        standardIdentifierAuthorityInput.value = standardIdentifierAuthority;

        // Standard identifier
        const standardIdentifierInput = correspondingRow.querySelector("input[name='standard_identifier']");
        standardIdentifierInput.value = standardIdentifier;

        const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll("input[name='standard_identifier_authority'], input[name='standard_identifier']"));
        checkAndSetRequiredAttributesForFields(
            conditionalRequiredFields,
            conditionalRequiredFields,
        );
    });
}

export function setupStandardIdentifiersTable() {
    const firstStandardIdentifiersTableRow = standardIdentifiersTableBody.querySelector("tr");
    loadPreviousData();
    setupRowEventListeners(firstStandardIdentifiersTableRow);
    setupAddStandardIdentifierRowButton();
}