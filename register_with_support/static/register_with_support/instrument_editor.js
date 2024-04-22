import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    setupCitationSection,
} from "/static/register_with_support/components/citation_section.js";
import {
    prepareOperationalModesJSON,
    prepareRelatedPartiesJSON,
} from "/static/register_with_support/components/json_field_processing.js";
import {
    setupOperationalModesTable,
} from "/static/register_with_support/components/instrument/operational_modes_table.js";

function prepareFormForSubmission() {
    prepareOperationalModesJSON();
    prepareRelatedPartiesJSON();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupCitationSection();
    setupOperationalModesTable();
});