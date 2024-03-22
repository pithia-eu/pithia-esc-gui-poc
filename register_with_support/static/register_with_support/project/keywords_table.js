import {
    inputSupportForm,
} from "/static/register_with_support/no_file_register_form.js";

const addKeywordsRowButton = document.getElementById("add-kwrow-button");

function getKeywordTableRowByChildNode(childNode) {
    const keywordsTable = inputSupportForm.querySelector("#table-project-keywords");
    const keywordsTableRows = keywordsTable.querySelectorAll("tbody tr");
    for (const row of keywordsTableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
}

function checkRemainingKeywordInputsOfRow(tableRow) {
    const keywordInputs = tableRow.querySelectorAll("input[name='keyword']");
}

function setupRemoveKeywordButton(removeKeywordButton) {
    removeKeywordButton.addEventListener("click", () => {
        const containingTableRow = getKeywordTableRowByChildNode(removeKeywordButton);
        const keywordsListElement = containingTableRow.querySelector("ul");
        const keywordLiElements = keywordsListElement.querySelectorAll("li");
        for (const liElement of keywordLiElements) {
            if (liElement.contains(removeKeywordButton)) {
                keywordsListElement.removeChild(liElement);
                break;
            }
        }
    });
}

function setupAddKeywordButton(addKeywordButton) {
    addKeywordButton.addEventListener("click", () => {
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
    });
}

function setupAddKeywordsRowButton() {
    addKeywordsRowButton.addEventListener("click", () => {
        const keywordsTableBody = inputSupportForm.querySelector("#table-project-keywords tbody");
        const keywordsTableFirstRow = keywordsTableBody.querySelector("tr");
        const newRow = document.createElement("TR");
        newRow.innerHTML = keywordsTableFirstRow.innerHTML;
        const newRowKeywordsList = newRow.querySelector("td.td-keywords ul");
        if (newRowKeywordsList.querySelectorAll("li").length > 0) {
            newRowKeywordsList.innerHTML = newRowKeywordsList.querySelector("li").outerHTML;
        }
        const newRowHighlightedInputs = newRow.querySelectorAll("input.was-validated");
        console.log('newRowHighlightedInputs', newRowHighlightedInputs);
        newRowHighlightedInputs.forEach(input => {
            input.classList.remove("was-validated");
            input.classList.remove("is-invalid");
        });
        keywordsTableBody.appendChild(newRow);
    });
}

export function setupKeywordsTable() {
    setupAddKeywordsRowButton();
    const keywordsTable = document.getElementById("table-project-keywords");
    const keywordsTableRows = keywordsTable.querySelectorAll("tbody tr");
    keywordsTableRows.forEach(row => {
        const addKeywordButton = row.querySelector(".add-kw-button");
        setupAddKeywordButton(addKeywordButton);
        const removeKeywordButton = row.querySelector(".remove-kw-button");
        setupRemoveKeywordButton(removeKeywordButton);
    });
}