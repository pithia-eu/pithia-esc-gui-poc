import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareKeywordsJSON,
} from "/static/register_with_support/components/json_field_processing.js";

const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

const keywordsTable = editorForm.querySelector("#table-project-keywords");
const keywordsTableBody = keywordsTable.querySelector("tbody");
const addKeywordsRowButton = document.getElementById("add-kwrow-button");

function getKeywordTableRowByChildNode(childNode) {
    const keywordsTableRows = keywordsTable.querySelectorAll("tbody tr");
    for (const row of keywordsTableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
}

function getNumRemainingKeywordInputsOfRow(tableRow) {
    return tableRow.querySelectorAll("input[name='keyword']").length;
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


function removeKeyword(liChildElement) {
    const containingTableRow = getKeywordTableRowByChildNode(liChildElement);
    const keywordsListElement = containingTableRow.querySelector("ul");
    const keywordLiElements = keywordsListElement.querySelectorAll("li");
    for (const liElement of keywordLiElements) {
        if (liElement.contains(liChildElement)) {
            keywordsListElement.removeChild(liElement);
            break;
        }
    }
    const remainingKeywordInputsInRow = getNumRemainingKeywordInputsOfRow(containingTableRow);
    if (remainingKeywordInputsInRow === 1) {
        containingTableRow.querySelector(".td-keywords .remove-kw-button").disabled = true;
    }
}

function setupRemoveKeywordButton(removeKeywordButton) {
    removeKeywordButton.addEventListener("click", e => {
        removeKeyword(e.currentTarget);
        prepareKeywordsJSON();
    });
}

function addKeyword(rowChildElement) {
    // Copy the first keyword input HTML to
    // add a new keyword input.
    const containingTableRow = getKeywordTableRowByChildNode(rowChildElement);
    const keywordsListElement = containingTableRow.querySelector("ul");
    const firstKeywordLiElement = keywordsListElement.querySelector("li");
    const newKeywordLiElement = document.createElement("li");
    newKeywordLiElement.classList = firstKeywordLiElement.classList;
    newKeywordLiElement.innerHTML = firstKeywordLiElement.innerHTML;
    const keywordInput = newKeywordLiElement.querySelector("input");
    keywordInput.value = "";
    keywordInput.addEventListener("input", () => {
        prepareKeywordsJSON();
    });

    // Ensure any IDs in the copied HTML are
    // not duplicated
    const childElementsWithIdAttribute = newKeywordLiElement.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const keywordLabel = containingTableRow.querySelector(`label[for="${elem.id}"]`);
        elem.id = newId;
        if (keywordLabel) {
            elem.setAttribute("aria-label", keywordLabel.innerHTML);
        }
    });

    // Setup the remove button
    const removeKeywordButton = newKeywordLiElement.querySelector(".remove-kw-button");
    removeKeywordButton.disabled = false;
    setupRemoveKeywordButton(removeKeywordButton);

    // Add the new keyword input
    keywordsListElement.appendChild(newKeywordLiElement);

    // Enable the first remove keyword button
    // if not enabled already as there are
    // more than two inputs now.
    const remainingKeywordInputsInRow = getNumRemainingKeywordInputsOfRow(containingTableRow);
    if (remainingKeywordInputsInRow > 1) {
        containingTableRow.querySelector(".td-keywords .remove-kw-button").disabled = false;
    }

    return newKeywordLiElement;
}

function setupAddKeywordButton(addKeywordButton) {
    addKeywordButton.addEventListener("click", e => {
        addKeyword(e.currentTarget);
        prepareKeywordsJSON();
    });
}

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

function addKeywordsRow() {
    // Create a new table row by copying
    // the first table row.
    const keywordsTableFirstRow = keywordsTableBody.querySelector("tr");
    const newRow = document.createElement("TR");
    newRow.innerHTML = keywordsTableFirstRow.innerHTML;
    const newRowKeywordsList = newRow.querySelector("td.td-keywords ul");
    if (newRowKeywordsList.querySelectorAll("li").length > 0) {
        newRowKeywordsList.innerHTML = newRowKeywordsList.querySelector("li").outerHTML;
    }
    const newRowHighlightedInputs = newRow.querySelectorAll("input.was-validated");
    newRowHighlightedInputs.forEach(input => {
        input.classList.remove("was-validated");
        input.classList.remove("is-invalid");
    });
    const rowInputs = newRow.querySelectorAll("input[type='text']");
    rowInputs.forEach(input => {
        input.value = "";
    });
    const removeKeywordButton = newRow.querySelector(".remove-kw-button");
    removeKeywordButton.disabled = true;
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

    // Setup each of the row's event listeners
    setupRowEventListeners(newRow);

    // Add the row to the table
    keywordsTableBody.appendChild(newRow);

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
    const inputs = tableRow.querySelectorAll("input[type='text']");
    inputs.forEach(input => {
        input.addEventListener("input", () => {
            prepareKeywordsJSON();
        });
    });
}

function setupRowEventListeners(tableRow) {
    setupInputEventMappingForRow(tableRow);
    const addKeywordButton = tableRow.querySelector(".add-kw-button");
    setupAddKeywordButton(addKeywordButton);
    const removeKeywordButton = tableRow.querySelector(".remove-kw-button");
    setupRemoveKeywordButton(removeKeywordButton);
    const removeKeywordsRowButton = tableRow.querySelector(".remove-kwrow-button");
    setupRemoveKeywordsRowButton(removeKeywordsRowButton);
}

function loadPreviousData() {
    const previousData = JSON.parse(editorForm.querySelector("input[name='keywords_json']").value);
    if (!previousData) {
        return;
    }
    for (let i = 0; i < Object.keys(previousData).length - 1; i++) {
        addKeywordsRow();
    }
    let rowIndex = 1;
    for (const keywordObject of previousData) {
        const keywordType = keywordObject.type.codeListValue;
        const keywordTypeCode = keywordObject.type.codeList;
        const keywords = keywordObject.keywords;
        const correspondingRow = keywordsTableBody.querySelector(`tr:nth-of-type(${rowIndex})`);
        // Keyword type
        const keywordTypeInput = correspondingRow.querySelector("input[name='keyword_type']");
        keywordTypeInput.value = keywordType;
        // Keyword type code
        const keywordTypeCodeInput = correspondingRow.querySelector("input[name='keyword_type_code']");
        keywordTypeCodeInput.value = keywordTypeCode.replace("#", "");
        // Keywords
        const keywordInput = correspondingRow.querySelector("input[name='keyword']");
        keywordInput.value = keywords[0];
        if (keywords.length > 1) {
            for (let i = 1; i < keywords.length; i++) {
                const newKeywordLiElement = addKeyword(keywordInput);
                const correspondingKeywordInput = newKeywordLiElement.querySelector("input[name='keyword']");
                correspondingKeywordInput.value = keywords[i];
            }
        }
        rowIndex += 1;
    }
}

export function setupKeywordsTable() {
    const firstKeywordTableRow = keywordsTableBody.querySelector("tr");
    loadPreviousData();
    setupRowEventListeners(firstKeywordTableRow);
    setupAddKeywordsRowButton();
}