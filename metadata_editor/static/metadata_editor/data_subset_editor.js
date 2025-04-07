import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupDataSubsetSourcesTab,
} from "/static/metadata_editor/components/data_subset/data_subset_sources_tab.js";
import {
    setupSourceFileSharingMethodSwitching,
} from "/static/metadata_editor/components/data_subset/source_file_sharing_method_switching.js";
import {
    setupTimePeriodsTab,
} from "/static/metadata_editor/components/data_subset/result_times_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

let sourcesTab;
let timePeriodsTab;


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

    timePeriodsTab = setupTimePeriodsTab();
    sourcesTab = setupDataSubsetSourcesTab();
    setupSourceFileSharingMethodSwitching(sourcesTab);
});