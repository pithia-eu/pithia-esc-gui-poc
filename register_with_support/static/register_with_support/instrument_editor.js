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
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupOperationalModesTable,
} from "/static/register_with_support/components/instrument/operational_modes_table.js";

let operationalModesTable;
let relatedPartiesTable;


function prepareFormForSubmission() {
    operationalModesTable.exportTableDataToJsonAndStoreInOutputElement();
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupLocalIdAndNamespaceRelatedEventListeners();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    operationalModesTable = setupOperationalModesTable();
});