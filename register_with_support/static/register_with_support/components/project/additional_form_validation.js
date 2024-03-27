import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

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

export function checkCitationSectionValidity() {
    const citationDateInput = editorForm.querySelector("input[name='citation_publication_date']");
    if (!isCitationSectionValid()) {
        citationDateInput.classList.add("was-validated");
        citationDateInput.classList.add("is-invalid");
        citationDateInput.focus();
        return false;
    }
    citationDateInput.classList.remove("was-validated");
    citationDateInput.classList.remove("is-invalid");
    return true;
}

function validateKeywordsTableAndReturnInvalidInputs() {
    const keywordsTableRows = Array.from(editorForm.querySelectorAll("#table-project-keywords tbody tr"));
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

export function checkKeywordsSectionValidity() {
    const invalidInputs = validateKeywordsTableAndReturnInvalidInputs();
    const validatedInputs = editorForm.querySelectorAll("#table-project-keywords tbody tr input.was-validated");
    validatedInputs.forEach(input => {
        input.classList.remove("was-validated");
        input.classList.remove("is-invalid");
    });
    invalidInputs.forEach(input => {
        input.classList.add("was-validated");
        input.classList.add("is-invalid");
    });
    if (invalidInputs.length > 0) {
        invalidInputs[0].focus();
        return false;
    }
    return true;
}

function validateRelatedPartiesTableAndReturnInvalidSelects() {
    const relatedPartiesTableRows = Array.from(editorForm.querySelectorAll("#table-related-parties tbody tr"));
    let invalidSelects = [];
    for (const row of relatedPartiesTableRows) {
        const roleSelect = row.querySelector("td:nth-of-type(1) select");
        const partySelects = Array.from(row.querySelectorAll("td:nth-of-type(2) select"));
        if (!roleSelect) {
            continue;
        }
        if (!(roleSelect.value.length > 0)
            && !(partySelects.every(select => select.value.length > 0))) {
            continue;
        }
        if (!roleSelect.value.length > 0) {
            invalidSelects.push(roleSelect);
        }
        if (!partySelects.some(select => select.value.length > 0)) {
            invalidSelects.push(partySelects[0]);
        }
    }
    return invalidSelects;
}

export function checkRelatedPartiesSectionValidity() {
    const invalidSelects = validateRelatedPartiesTableAndReturnInvalidSelects();
    const validatedSelects = editorForm.querySelectorAll("#table-related-parties tbody tr select.was-validated");
    validatedSelects.forEach(input => {
        input.classList.remove("was-validated");
        input.classList.remove("is-invalid");
    });
    invalidSelects.forEach(input => {
        input.classList.add("was-validated");
        input.classList.add("is-invalid");
    });
    if (invalidSelects.length > 0) {
        invalidSelects[0].focus();
        return false;
    }
    return true;
}