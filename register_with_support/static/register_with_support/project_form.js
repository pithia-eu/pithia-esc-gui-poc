import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/localid_validation.js";
import {
    inputSupportForm,
    validateAndRegister,
} from "/static/register_with_support/no_file_register_form.js";

function prepareKeywordsJSON() {
    const keywordsCategorised = {};
    const keywordsTableRows = document.querySelectorAll("#table-project-keywords tbody tr");
    keywordsTableRows.forEach(row => {
        const keywordTypeInput = row.querySelector("input[name='keyword_type']");
        const keywordTypeCodeInput = row.querySelector("input[name='keyword_type_code']");
        const keywordsForTypeInputs = Array.from(row.querySelectorAll("input[name='keyword']"));
        if (keywordTypeInput) {
            keywordsCategorised[keywordTypeInput.value] = {
                code: "#" + keywordTypeCodeInput.value,
                keywords: keywordsForTypeInputs.map(keywordInput => keywordInput.value),
            }
            console.log("keywordsCategorised[keywordTypeInput.value]", keywordsCategorised[keywordTypeInput.value]);
        }
    });
    const keywordsHiddenInput = document.querySelector("input[name='keywords_dict']");
    keywordsHiddenInput.value = JSON.stringify(keywordsCategorised);
}

function prepareFormForSubmission() {
    prepareKeywordsJSON();
}

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
});