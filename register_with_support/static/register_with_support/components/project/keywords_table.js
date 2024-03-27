import {
    inputSupportForm,
} from "/static/register_with_support/components/no_file_register_form.js";

const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

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

function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
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
    // Copy the first keyword input HTML to
    // add a new keyword input.
    const addKeywordButton = event.currentTarget;
    const containingTableRow = getKeywordTableRowByChildNode(addKeywordButton);
    const keywordsListElement = containingTableRow.querySelector("ul");
    const firstKeywordLiElement = keywordsListElement.querySelector("li");
    const newKeywordLiElement = document.createElement("li");
    newKeywordLiElement.classList = firstKeywordLiElement.classList;
    newKeywordLiElement.innerHTML = firstKeywordLiElement.innerHTML;

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