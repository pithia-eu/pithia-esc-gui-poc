import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCitationsTab,
} from "/static/metadata_editor/components/citations_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupKeywordsTable,
} from "/static/metadata_editor/components/project/keywords_table.js";

// let keywordsTable;
let relatedPartiesTable;


function prepareFormForSubmission() {
    // keywordsTable.exportTableDataToJsonAndStoreInOutputElement();
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    prepareFormForSubmission();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupCitationsTab();
    // keywordsTable = setupKeywordsTable();
    relatedPartiesTable = setupRelatedPartiesTable();
});