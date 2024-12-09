import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCatalogueDataSubsetSourcesTab,
} from "/static/metadata_editor/components/catalogue_data_subset/catalogue_data_subset_sources_tab.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const sourcesSharingMethodCheckbox = editorForm.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
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

    sourcesTab = setupCatalogueDataSubsetSourcesTab();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
});

sourcesSharingMethodCheckbox.addEventListener("change", () => {
    if (sourcesSharingMethodCheckbox.checked) {
        return sourcesTab.setSourceFileSharingMethodToLinkage();
    }
    return sourcesTab.setSourceFileSharingMethodToFileUpload();
});