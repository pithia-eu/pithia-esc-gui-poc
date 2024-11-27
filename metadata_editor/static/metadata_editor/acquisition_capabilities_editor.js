import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCapabilitiesTab,
} from "/static/metadata_editor/components/capabilities_tab.js";
import {
    setupCitationSection,
} from "/static/metadata_editor/components/citation_section.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupInstrumentModePairSection,
} from "/static/metadata_editor/components/acquisition_capabilities/instrument_mode_pair_section.js";
import {
    setupInputDescriptionsTable,
} from "/static/metadata_editor/components/acquisition_capabilities/input_descriptions_table.js";

let relatedPartiesTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    prepareFormForSubmission();
    await validateAndRegister();
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    setupCitationSection();
    relatedPartiesTable = setupRelatedPartiesTable();
    setupInputDescriptionsTable();
    setupCapabilitiesTab();
    setupInstrumentModePairSection();
    setupQualityAssessmentSection();
});