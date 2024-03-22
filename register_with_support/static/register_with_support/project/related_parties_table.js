import {
    inputSupportForm,
} from "/static/register_with_support/no_file_register_form.js";

const relatedPartiesTable = inputSupportForm.querySelector("#table-related-parties");
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

function setupRemoveRelatedPartyButton(removeRelatedPartyButton) {
    removeRelatedPartyButton.addEventListener("click", () => {
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
    });
}

function setupAddRelatedPartyButton(addRelatedPartyButton) {
    addRelatedPartyButton.addEventListener("click", () => {
        const containingTableRow = getRelatedPartiesTableRowByChildNode(addRelatedPartyButton);
        const relatedPartiesListElement = containingTableRow.querySelector("ul");
        const firstRelatedPartyLiElement = relatedPartiesListElement.querySelector("li");
        const newRelatedPartyLiElement = document.createElement("li");
        newRelatedPartyLiElement.classList = firstRelatedPartyLiElement.classList;
        newRelatedPartyLiElement.innerHTML = firstRelatedPartyLiElement.innerHTML;
        const removeRelatedPartyButton = newRelatedPartyLiElement.querySelector(".remove-rp-button");
        removeRelatedPartyButton.disabled = false;
        setupRemoveRelatedPartyButton(removeRelatedPartyButton);
        relatedPartiesListElement.appendChild(newRelatedPartyLiElement);
        const remainingRelatedPartySelectsInRow = getNumRemainingRelatedPartySelectsOfRow(containingTableRow);
        if (remainingRelatedPartySelectsInRow > 1) {
            containingTableRow.querySelector(".td-related-parties .remove-rp-button").disabled = false;
        }
    });
}

function setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton) {
    removeRelatedPartyRoleButton.addEventListener("click", () => {
        const containingTableRow = getRelatedPartiesTableRowByChildNode(removeRelatedPartyRoleButton);
        relatedPartiesTableBody.removeChild(containingTableRow);
        const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
        if (numRemainingTableRows === 1) {
            const firstRemoveRowButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
            firstRemoveRowButton.disabled = true;
        }
    });
}

function setupAddRelatedPartyRoleButton() {
    addRelatedPartyRoleButton.addEventListener("click", () => {
        const relatedPartiesTableFirstRow = relatedPartiesTableBody.querySelector("tr");
        const newRow = document.createElement("TR");
        newRow.innerHTML = relatedPartiesTableFirstRow.innerHTML;
        const newRowRelatedPartiesList = newRow.querySelector("td.td-related-parties ul");
        if (newRowRelatedPartiesList.querySelectorAll("li").length > 0) {
            newRowRelatedPartiesList.innerHTML = newRowRelatedPartiesList.querySelector("li").outerHTML;
        }
        const newRowHighlightedInputs = newRow.querySelectorAll("input.was-validated");
        newRowHighlightedInputs.forEach(input => {
            input.classList.remove("was-validated");
            input.classList.remove("is-invalid");
        });
        const addRelatedPartyButton = newRow.querySelector(".add-rp-button");
        setupAddRelatedPartyButton(addRelatedPartyButton);
        const removeRelatedPartyButton = newRow.querySelector(".remove-rp-button");
        setupRemoveRelatedPartyButton(removeRelatedPartyButton);
        const removeRelatedPartyRoleButton = newRow.querySelector(".remove-rprrow-button");
        removeRelatedPartyRoleButton.disabled = false;
        setupRemoveRelatedPartyRoleButton(removeRelatedPartyRoleButton);
        relatedPartiesTableBody.appendChild(newRow);
        const numRemainingTableRows = getNumRemainingRelatedPartyRoles();
        if (numRemainingTableRows > 1) {
            const firstRemoveRoleButton = relatedPartiesTableBody.querySelector(".remove-rprrow-button");
            firstRemoveRoleButton.disabled = false;
        }
    });
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