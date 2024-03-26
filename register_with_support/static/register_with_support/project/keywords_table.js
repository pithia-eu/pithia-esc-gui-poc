import {
    inputSupportForm,
} from "/static/register_with_support/no_file_register_form.js";

const keywordsTable = inputSupportForm.querySelector("#table-project-keywords");
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


function removeKeyword(event) {
    const removeKeywordButton = event.currentTarget;
    const containingTableRow = getKeywordTableRowByChildNode(removeKeywordButton);
    const keywordsListElement = containingTableRow.querySelector("ul");
    const keywordLiElements = keywordsListElement.querySelectorAll("li");
    for (const liElement of keywordLiElements) {
        if (liElement.contains(removeKeywordButton)) {
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
    removeKeywordButton.addEventListener("click", removeKeyword);
}

function addKeyword(event) {
    const addKeywordButton = event.currentTarget;
    const containingTableRow = getKeywordTableRowByChildNode(addKeywordButton);
    const keywordsListElement = containingTableRow.querySelector("ul");
    const firstKeywordLiElement = keywordsListElement.querySelector("li");
    const newKeywordLiElement = document.createElement("li");
    newKeywordLiElement.classList = firstKeywordLiElement.classList;
    newKeywordLiElement.innerHTML = firstKeywordLiElement.innerHTML;
    const removeKeywordButton = newKeywordLiElement.querySelector(".remove-kw-button");
    removeKeywordButton.disabled = false;
    setupRemoveKeywordButton(removeKeywordButton);
    keywordsListElement.appendChild(newKeywordLiElement);
    const remainingKeywordInputsInRow = getNumRemainingKeywordInputsOfRow(containingTableRow);
    if (remainingKeywordInputsInRow > 1) {
        containingTableRow.querySelector(".td-keywords .remove-kw-button").disabled = false;
    }
}

function setupAddKeywordButton(addKeywordButton) {
    addKeywordButton.addEventListener("click", addKeyword);
}

function removeKeywordsRow(event) {
    const removeKeywordsRowButton = event.currentTarget;
    const containingTableRow = getKeywordTableRowByChildNode(removeKeywordsRowButton);
    keywordsTableBody.removeChild(containingTableRow);
    const numRemainingTableRows = getNumRemainingKeywordRows();
    if (numRemainingTableRows === 1) {
        const firstRemoveRowButton = keywordsTableBody.querySelector(".remove-kwrow-button");
        firstRemoveRowButton.disabled = true;
    }
}

function setupRemoveKeywordsRowButton(removeKeywordsRowButton) {
    removeKeywordsRowButton.addEventListener("click", removeKeywordsRow);
}

function addKeywordsRow(event) {
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

    // Ensure the IDs of any child elements are
    // unique.
    const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
    childElementsWithIdAttribute.forEach(elem => {
        const newId = `${elem.id}${Date.now()}`;
        const correspondingLabels = newRow.querySelectorAll(`label[for="${elem.id}"]`)
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
    });

    // Setup each of the row's buttons
    const addKeywordButton = newRow.querySelector(".add-kw-button");
    setupAddKeywordButton(addKeywordButton);
    const removeKeywordButton = newRow.querySelector(".remove-kw-button");
    setupRemoveKeywordButton(removeKeywordButton);
    const removeKeywordsRowButton = newRow.querySelector(".remove-kwrow-button");
    removeKeywordsRowButton.disabled = false;
    setupRemoveKeywordsRowButton(removeKeywordsRowButton);

    // Add the row to the table
    keywordsTableBody.appendChild(newRow);

    // Enable the first row's remove button
    // if it is not already enabled.
    const numRemainingTableRows = getNumRemainingKeywordRows();
    if (numRemainingTableRows > 1) {
        const firstRemoveRowButton = keywordsTableBody.querySelector(".remove-kwrow-button");
        firstRemoveRowButton.disabled = false;
    }
}

function setupAddKeywordsRowButton() {
    addKeywordsRowButton.addEventListener("click", addKeywordsRow);
}

export function setupKeywordsTable() {
    const keywordsTableRows = keywordsTableBody.querySelectorAll("tr");
    keywordsTableRows.forEach(row => {
        const addKeywordButton = row.querySelector(".add-kw-button");
        setupAddKeywordButton(addKeywordButton);
        const removeKeywordButton = row.querySelector(".remove-kw-button");
        setupRemoveKeywordButton(removeKeywordButton);
        if (getNumRemainingKeywordInputsOfRow(row) === 1) {
            removeKeywordButton.disabled = true;
        }
        const removeKeywordsRowButton = document.querySelector(".remove-kwrow-button");
        setupRemoveKeywordsRowButton(removeKeywordsRowButton);
        if (keywordsTableRows.length === 1) {
            removeKeywordsRowButton.disabled = true;
        }
    });
    setupAddKeywordsRowButton();
}