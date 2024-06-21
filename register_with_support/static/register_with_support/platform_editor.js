import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupCitationSection,
} from "/static/register_with_support/components/citation_section.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";
import {
    setupGeometryLocationSection,
} from "/static/register_with_support/components/geometry_location_section.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupPlatformStandardIdentifiersTable,
} from "/static/register_with_support/components/platform/platform_standard_identifiers_table.js";

let relatedPartiesTable;
let platformStandardIdentifiersTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
    platformStandardIdentifiersTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupCitationSection();
    setupGeometryLocationSection();
    setupLocalIdAndNamespaceRelatedEventListeners();
    relatedPartiesTable = setupRelatedPartiesTable();
    platformStandardIdentifiersTable = setupPlatformStandardIdentifiersTable();
});