import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupSourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

let sourcesTab;


function prepareFormForSubmission() {
    sourcesTab.exportTabData();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    prepareFormForSubmission();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    sourcesTab = setupSourcesTab();
    setupRelatedPartiesTable();
    setupQualityAssessmentSection();
});