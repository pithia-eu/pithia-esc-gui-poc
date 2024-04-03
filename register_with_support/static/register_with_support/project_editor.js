import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareKeywordsJSON,
    prepareRelatedPartiesJSON,
} from "/static/register_with_support/components/json_field_processing.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    checkCitationSectionValidity,
    checkKeywordsSectionValidity,
    checkRelatedPartiesSectionValidity,
} from "/static/register_with_support/components/project/additional_form_validation.js";
import {
    setupKeywordsTable,
} from "/static/register_with_support/components/project/keywords_table.js";

function prepareFormForSubmission() {
    prepareKeywordsJSON();
    prepareRelatedPartiesJSON();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    // Run custom form validation
    const checks = [
        checkCitationSectionValidity(),
        checkKeywordsSectionValidity(),
        checkRelatedPartiesSectionValidity(),
    ];
    if (checks.some(check => check === false)) {
        return false;
    }

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupKeywordsTable();
    setupRelatedPartiesTable();
});