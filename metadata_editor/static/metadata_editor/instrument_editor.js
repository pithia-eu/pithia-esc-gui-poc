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
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupOperationalModesTable,
} from "/static/metadata_editor/components/instrument/operational_modes_table.js";

let operationalModesTable;
let relatedPartiesTable;


function prepareFormForSubmission() {
    operationalModesTable.exportTableDataToJsonAndStoreInOutputElement();
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    prepareFormForSubmission();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    operationalModesTable = setupOperationalModesTable();
});