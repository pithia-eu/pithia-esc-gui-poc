import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/localid_validation.js";
import {
    inputSupportForm,
    validateAndRegister,
} from "/static/register_with_support/no_file_register_form.js";
const addKeywordsRowButton = document.getElementById("add-kwrow-button");

function prepareKeywordsJSON() {
    const keywordsCategorised = {};
    const keywordsTableRows = document.querySelectorAll("#table-project-keywords tbody tr");
    keywordsTableRows.forEach(row => {
        const keywordTypeInput = row.querySelector("input[name='keyword_type']");
        if (keywordTypeInput.value) {
            const keywordTypeCodeInput = row.querySelector("input[name='keyword_type_code']");
            const keywordsForTypeInputs = Array.from(row.querySelectorAll("input[name='keyword']"));
            keywordsCategorised[keywordTypeInput.value] = {
                code: "#" + keywordTypeCodeInput.value,
                keywords: keywordsForTypeInputs.map(keywordInput => keywordInput.value),
            }
        }
    });
    const keywordsHiddenInput = document.querySelector("input[name='keywords_json']");
    keywordsHiddenInput.value = JSON.stringify(keywordsCategorised);
}

function prepareRelatedPartiesJSON() {
    const relatedPartiesCategorised = {};
    const relatedPartyTableRows = document.querySelectorAll("#table-related-parties tbody tr");
    relatedPartyTableRows.forEach(row => {
        const relatedPartyRoleSelect = row.querySelector("select[name='related_party_role']");
        if (relatedPartyRoleSelect !== null && relatedPartyRoleSelect.value) {
            const relatedPartySelects = Array.from(row.querySelectorAll("select[name='related_party']"));
            relatedPartiesCategorised[relatedPartyRoleSelect.value] = relatedPartySelects.map(select => select.value);
        }
    });
    const relatedPartiesHiddenInput = document.querySelector("input[name='related_parties_json']");
    relatedPartiesHiddenInput.value = JSON.stringify(relatedPartiesCategorised);
}

function prepareFormForSubmission() {
    prepareKeywordsJSON();
    prepareRelatedPartiesJSON();
}

function isCitationSectionValid() {
    const citationDateInput = document.querySelector("#citation-section input[name='citation_publication_date']");
    const otherCitationSectionInputs = Array.from(document.querySelectorAll("#citation-section input:not([name='citation_publication_date'])"));
    const citationSectionTextarea = document.querySelector("#citation-section textarea");

    if (citationDateInput.value.length === 0
        && otherCitationSectionInputs.every(input => input.value.length === 0
        && citationSectionTextarea.value.length === 0)) {
            return true;
        }

    const isNonCitationDateFieldFilled = otherCitationSectionInputs.some(input => input.value.length > 0) || citationSectionTextarea.value.length > 0;

    return citationDateInput.value.length > 0 && isNonCitationDateFieldFilled;
}

function checkCitationSectionValidity() {
    const citationDateInput = inputSupportForm.querySelector("input[name='citation_publication_date']");
    if (!isCitationSectionValid()) {
        citationDateInput.classList.add("was-validated");
        citationDateInput.classList.add("is-invalid");
        citationDateInput.focus();
        return false;
    } else {
        citationDateInput.classList.remove("was-validated");
        citationDateInput.classList.remove("is-invalid");
    }
}

function validateKeywordsTableAndReturnInvalidInputs() {
    const keywordsTableRows = Array.from(inputSupportForm.querySelectorAll("#table-project-keywords tbody tr"));
    let invalidInputs = [];
    for (const row of keywordsTableRows) {
        const keywordTypeInput = row.querySelector("td:nth-of-type(1) input");
        const keywordTypeCodeInput = row.querySelector("td:nth-of-type(2) input");
        const keywordInputs = Array.from(row.querySelectorAll("td:nth-of-type(3) input"));
        if (!keywordTypeInput) {
            continue;
        }
        if (!(keywordTypeInput.value.length > 0)
            && !(keywordTypeCodeInput.value.length > 0)
            && !(keywordInputs.every(input => input.value.length > 0))) {
            continue;
        }
        if (!keywordTypeInput.value.length > 0) {
            invalidInputs.push(keywordTypeInput);
        }
        if (!keywordTypeCodeInput.value.length > 0) {
            invalidInputs.push(keywordTypeCodeInput);
        }
        if (!keywordInputs.some(input => input.value.length > 0)) {
            invalidInputs.push(keywordInputs[0]);
        }
    }
    return invalidInputs;
}

function checkKeywordsSectionValidity() {
    const invalidInputs = validateKeywordsTableAndReturnInvalidInputs();
    const validatedInputs = inputSupportForm.querySelectorAll("#table-project-keywords tbody tr input.was-validated");
    validatedInputs.forEach(input => {
        input.classList.remove("was-validated");
        input.classList.remove("is-invalid");
    });
    invalidInputs.forEach(input => {
        input.classList.add("was-validated");
        input.classList.add("is-invalid");
    });
    if (invalidInputs.length > 0) invalidInputs[0].focus();
}

function isRelatedPartiesSectionValid() {

}

function checkRelatedPartiesSectionValidity() {

}


addKeywordsRowButton.addEventListener("click", () => {
    const keywordsTableBody = inputSupportForm.querySelector("#table-project-keywords tbody");
    const keywordsTableFirstRow = keywordsTableBody.querySelector("tr");
    const newRow = document.createElement("TR");
    newRow.innerHTML = keywordsTableFirstRow.innerHTML;
    const newRowKeywordsList = newRow.querySelector("td:last-of-type ul");
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

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    // Run custom form validation
    checkCitationSectionValidity();
    checkKeywordsSectionValidity();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
});