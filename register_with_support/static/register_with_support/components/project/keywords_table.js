import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareKeywordsJSON,
} from "/static/register_with_support/components/json_field_processing.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";

const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

const keywordsTable = editorForm.querySelector("#table-project-keywords");
const keywordsTableBody = keywordsTable.querySelector("tbody");
const addKeywordsRowButton = document.getElementById("add-kwrow-button");
const keywordsTableRowContentTemplate = JSON.parse(document.getElementById("keywords-row-content-template").textContent);


// Util functions
function getKeywordTableRowByChildNode(childNode) {
    const keywordsTableRows = keywordsTable.querySelectorAll("tbody tr");
    for (const row of keywordsTableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
}

function getNumRemainingKeywordRows() {
    return keywordsTableBody.querySelectorAll("tr").length;
}

function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
}


// Table management functions
function removeKeywordsRow(rowChildElement) {
    const containingTableRow = getKeywordTableRowByChildNode(rowChildElement);
    keywordsTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingKeywordRows();
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = keywordsTableBody.querySelector(".remove-kwrow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveKeywordsRowButton(removeKeywordsRowButton) {
    removeKeywordsRowButton.addEventListener("click", e => {
        removeKeywordsRow(e.currentTarget);
        prepareKeywordsJSON();
    });
}

function setupDuplicatedKeywordsRow(newRow) {
    const removeKeywordsRowButton = newRow.querySelector(".remove-kwrow-button");
    removeKeywordsRowButton.disabled = false;

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

function addKeywordsRow() {
    // Create a new table row using the template
    // HTML
    const newRow = document.createElement("TR");
    newRow.innerHTML = keywordsTableRowContentTemplate;

    // Reset any unique values which may have been
    // duplicated
    setupDuplicatedKeywordsRow(newRow);

    // Setup each of the row's event listeners
    setupRowEventListeners(newRow);

    // Add the row to the table
    keywordsTableBody.appendChild(newRow);

    window.dispatchEvent(new CustomEvent("newKeywordsSelectsAdded", {
        detail: Array.from(newRow.querySelectorAll("select[name='keyword']")).map(select => select.id),
    }));

    // Enable the first row's remove button
    // if it is not already enabled.
    const numRemainingTableRows = getNumRemainingKeywordRows();
    if (numRemainingTableRows > 1) {
        const firstRemoveRowButton = keywordsTableBody.querySelector(".remove-kwrow-button");
        firstRemoveRowButton.disabled = false;
    }

    return newRow;
}

function setupAddKeywordsRowButton() {
    addKeywordsRowButton.addEventListener("click", () => {
        addKeywordsRow();
        prepareKeywordsJSON();
    });
}

function setupInputEventMappingForRow(tableRow) {
    const inputs = Array.from(tableRow.querySelectorAll("input[name='keyword_type'], input[name='keyword_type_code']"));
    const selects = Array.from(tableRow.querySelectorAll("select"));
    const allFields = [
        ...inputs,
        ...selects,
    ];
    inputs.forEach(input => {
        input.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(allFields, allFields);
            prepareKeywordsJSON();
        });
    });
    selects.forEach(select => {
        select.addEventListener("change", () => {
            checkAndSetRequiredAttributesForFields(allFields, allFields);
            prepareKeywordsJSON();
        });
    });
}

function setupRowEventListeners(tableRow) {
    setupInputEventMappingForRow(tableRow);
    const removeKeywordsRowButton = tableRow.querySelector(".remove-kwrow-button");
    setupRemoveKeywordsRowButton(removeKeywordsRowButton);
}

function loadPreviousData() {
    const previousData = JSON.parse(editorForm.querySelector("input[name='keywords_json']").value);
    if (!previousData) {
        return;
    }
    for (let i = 0; i < previousData.length - 1; i++) {
        addKeywordsRow();
    }
    previousData.forEach((keywordObject, i) => {
        const keywordType = keywordObject.type.codeListValue;
        const keywordTypeCode = keywordObject.type.codeList;
        const keywords = keywordObject.keywords;
        const correspondingRow = keywordsTableBody.querySelector(`tr:nth-of-type(${i + 1})`);

        // Keyword type
        const keywordTypeInput = correspondingRow.querySelector("input[name='keyword_type']");
        keywordTypeInput.value = keywordType;

        // Keyword type code
        const keywordTypeCodeInput = correspondingRow.querySelector("input[name='keyword_type_code']");
        keywordTypeCodeInput.value = keywordTypeCode.replace("#", "");

        // Keywords
        // Populate the keyword select with the
        // data saved to the JSON field
        const keywordMultipleChoiceSelect = correspondingRow.querySelector("select[name='keyword']");
        keywords.forEach((kw, kwi) => {
            keywordMultipleChoiceSelect.options[kwi] = new Option(kw, kw);
            keywordMultipleChoiceSelect.querySelector(`option[value="${kw}"]`).selected = true;
        });
        window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
            detail: keywordMultipleChoiceSelect.id,
        }));
        const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll("input[name='keyword_type'], input[name='keyword_type_code'], select"));
        checkAndSetRequiredAttributesForFields(
            conditionalRequiredFields,
            conditionalRequiredFields,
        );
    });
}

export function setupKeywordsTable() {
    const firstKeywordTableRow = keywordsTableBody.querySelector("tr");
    loadPreviousData();
    setupRowEventListeners(firstKeywordTableRow);
    setupAddKeywordsRowButton();
}