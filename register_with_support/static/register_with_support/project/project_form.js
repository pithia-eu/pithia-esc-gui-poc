import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/localid_validation.js";
import {
    inputSupportForm,
    validateAndRegister,
} from "/static/register_with_support/no_file_register_form.js";
import {
    checkCitationSectionValidity,
    checkKeywordsSectionValidity,
} from "/static/register_with_support/project/additional_form_validation.js";
import {
    setupKeywordsTable,
} from "/static/register_with_support/project/keywords_table.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/project/related_parties_table.js";

function prepareKeywordsJSON() {
    const keywordsCategorised = {};
    const keywordsTableRows = document.querySelectorAll("#table-project-keywords tbody tr");
    keywordsTableRows.forEach(row => {
        const keywordTypeInput = row.querySelector("input[name='keyword_type']");
        if (keywordTypeInput.value.trim() !== "") {
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
        if (relatedPartyRoleSelect !== null && relatedPartyRoleSelect.value.trim() !== "") {
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
    setupKeywordsTable();
    setupRelatedPartiesTable();
});