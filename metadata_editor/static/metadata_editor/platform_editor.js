import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/metadata_editor/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCitationSection,
} from "/static/metadata_editor/components/citation_section.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupGeometryLocationSection,
} from "/static/metadata_editor/components/geometry_location_section.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupPlatformStandardIdentifiersTable,
} from "/static/metadata_editor/components/platform/platform_standard_identifiers_table.js";

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

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    await setupLocalIdAndNamespaceRelatedEventListeners();
    setupCitationSection();
    setupGeometryLocationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    platformStandardIdentifiersTable = setupPlatformStandardIdentifiersTable();
});