import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupDataSubsetUpdateSourcesTab,
} from "/static/update_with_support/components/data_subset/data_subset_update_sources_tab.js";
import {
    setupSourceFileSharingMethodSwitching,
} from "/static/metadata_editor/components/data_subset/source_file_sharing_method_switching.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
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

    sourcesTab = setupDataSubsetUpdateSourcesTab();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
    setupSourceFileSharingMethodSwitching(sourcesTab);
});