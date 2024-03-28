import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    prepareRelatedPartiesJSON,
} from "/static/register_with_support/components/json_field_processing.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    checkRelatedPartiesSectionValidity,
} from "/static/register_with_support/components/additional_form_validation.js";
import {
    setupChildPlatformsList,
} from "/static/register_with_support/components/platform/child_platforms.js";

function prepareFormForSubmission() {
    prepareRelatedPartiesJSON();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    // Run custom form validation
    if (!checkRelatedPartiesSectionValidity()) {
        return false;
    }

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupRelatedPartiesTable();
    setupChildPlatformsList();
});