import {
    generateUniqueElemIdFromCurrentElemId,
    getTableRowByChildNode,
    getNumRemainingRowsInTable,
} from "/static/register_with_support/components/table_utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
import {
    prepareOperationalModesJSON,
} from "/static/register_with_support/components/json_field_processing.js";

const operationalModesTable = document.getElementById("table-operational-modes");
const operationalModesTableBody = operationalModesTable.querySelector("tbody");
const operationalModeTableRowTemplateContent = JSON.parse(document.getElementById("operational-mode-row-content-template").textContent);
const addRowButton = document.getElementById("add-omrow-button");


function removeOperationalModeRow(rowChildElement) {
    const containingTableRow = getTableRowByChildNode(operationalModesTableBody, rowChildElement);
    operationalModesTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingRowsInTable(operationalModesTableBody);
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = operationalModesTableBody.querySelector(".remove-omrow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveOperationalModeRowButton(removeOperationalModeRowButton) {
    removeOperationalModeRowButton.addEventListener("click", e => {
        removeOperationalModeRow(e.currentTarget);
        prepareOperationalModesJSON();
    });
}

function setupOperationalModeDescriptionTextarea(tableRow) {
    const operationalModeDescriptionTextarea = tableRow.querySelector("textarea[name='operational_mode_description']");
    const operationalModeDescriptionDiv = tableRow.querySelector("textarea[name='operational_mode_description'] ~ div");

    operationalModeDescriptionTextarea.addEventListener("focus", () => {
        operationalModeDescriptionTextarea.style.height = operationalModeDescriptionTextarea.scrollHeight + "px";
    });
    
    operationalModeDescriptionTextarea.addEventListener("input", () => {
        operationalModeDescriptionTextarea.style.height = operationalModeDescriptionTextarea.scrollHeight + "px";
        operationalModeDescriptionDiv.innerHTML = operationalModeDescriptionTextarea.value;
        prepareOperationalModesJSON();
    });
    
    operationalModeDescriptionTextarea.addEventListener("blur", () => {
        operationalModeDescriptionTextarea.removeAttribute("style");
    });
}

function setupInputEventMappingForRow(tableRow) {
    const fields = Array.from(tableRow.querySelectorAll("input[name='operational_mode_id'], input[name='operational_mode_name'], textarea[name='operational_mode_description']"));
    fields.forEach(field => {
            field.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(fields, fields);
            prepareOperationalModesJSON();
        });
    });
}

function setupTableRowEventListeners(tableRow) {
    setupInputEventMappingForRow(tableRow);
    setupOperationalModeDescriptionTextarea(tableRow);
    const removeOperationalModeRowButton = tableRow.querySelector(".remove-omrow-button");
    setupRemoveOperationalModeRowButton(removeOperationalModeRowButton);
}

function setupDuplicatedTableRow(newRow) {
    const removeTableRowButton = newRow.querySelector(".remove-omrow-button");
    removeTableRowButton.disabled = false;

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

function addOperationalModeRow() {
    const newRow = document.createElement("TR");
    newRow.innerHTML = operationalModeTableRowTemplateContent;

    setupDuplicatedTableRow(newRow);

    setupTableRowEventListeners(newRow);

    operationalModesTableBody.appendChild(newRow);

    const numRemainingTableRows = getNumRemainingRowsInTable(operationalModesTableBody);
    if (numRemainingTableRows > 1) {
        const firstRemoveRowButton = operationalModesTableBody.querySelector(".remove-omrow-button");
        firstRemoveRowButton.disabled = false;
    }

    return newRow;
}

function setupAddRowButton() {
    addRowButton.addEventListener("click", () => {
        addOperationalModeRow();
        prepareOperationalModesJSON();
    });
}

function loadPreviousData() {
    const previousData = JSON.parse(document.querySelector("input[name='operational_modes_json']").value);
    if (!previousData) {
        return;
    }
    for (let i = 0; i < previousData.length - 1; i++) {
        addOperationalModeRow();
    }
    previousData.forEach((operationalModeObject, i) => {
        const operationalModeId = operationalModeObject.id;
        const operationalModeName = operationalModeObject.name;
        const operationalModeDescription = operationalModeObject.description;
        const correspondingRow = operationalModesTableBody.querySelector(`tr:nth-of-type(${i + 1})`);

        // Operational mode ID
        const operationalModeIdInput = correspondingRow.querySelector("input[name='operational_mode_id']");
        operationalModeIdInput.value = operationalModeId;

        // Operational mode name
        const operationalModeNameInput = correspondingRow.querySelector("input[name='operational_mode_name']");
        operationalModeNameInput.value = operationalModeName;

        // Operational mode description
        const operationalModeDescriptionTextarea = correspondingRow.querySelector("textarea[name='operational_mode_description']");
        const operationalModeDescriptionDiv = correspondingRow.querySelector("textarea[name='operational_mode_description'] ~ div");
        operationalModeDescriptionTextarea.value = operationalModeDescription;
        operationalModeDescriptionDiv.innerHTML = operationalModeDescription;

        const conditionalRequiredFields = [
            operationalModeIdInput,
            operationalModeNameInput,
            operationalModeDescriptionTextarea,
        ];
        checkAndSetRequiredAttributesForFields(
            conditionalRequiredFields,
            conditionalRequiredFields
        );
    });
}

export function setupOperationalModesTable() {
    const firstOperationalModeTableRow = operationalModesTableBody.querySelector("tr");
    loadPreviousData();
    setupTableRowEventListeners(firstOperationalModeTableRow);
    setupAddRowButton();
}