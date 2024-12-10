import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCatalogueDataSubsetUpdateSourcesTab,
} from "/static/update_with_support/components/catalogue_data_subset/catalogue_data_subset_update_sources_tab.js";
import {
    setupSourceFileSharingMethodSwitching,
} from "/static/metadata_editor/components/catalogue_data_subset/source_file_sharing_method_switching.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

let sourcesTab;


function addDataHubStatusesToSourcesData() {
    let dataHubUsageStatuses = [];
    try {
        // JSON.parse twice as the sources JSON
        // was JSONified again when added to HTML
        // using json_script Django filter.
        const sourcesDefault = JSON.parse(JSON.parse(document.querySelector("#sources-default").textContent));
        dataHubUsageStatuses = sourcesDefault.reduce((accumulator, source) => {
            if (!("isSourceFileInDataHub" in source)) {
                accumulator[source.name] = false;
                return accumulator;
            }
            accumulator[source.name] = source.isSourceFileInDataHub;
            return accumulator;
        }, {});
    } catch (error) {
        // Sources JSON element is null
        // or not JSON-parsable.
        console.error(error);
    }

    // Add DataHub usage statuses
    const sourcesJsonElement = editorForm.querySelector("input[name='sources_json']");
    const sourcesData = JSON.parse(sourcesJsonElement.value);
    for (const sourceName in dataHubUsageStatuses) {
        const sourceIndex = sourcesData.findIndex(source => source.name === sourceName);
        if (sourceIndex === -1) {
            continue;
        }
        const dataHubUsageStatusForSource = dataHubUsageStatuses[sourceName];
        sourcesData[sourceIndex].isSourceFileInDataHub = dataHubUsageStatusForSource;
    }
    sourcesJsonElement.value = JSON.stringify(sourcesData);
}

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
    addDataHubStatusesToSourcesData();

    sourcesTab = setupCatalogueDataSubsetUpdateSourcesTab();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
    setupSourceFileSharingMethodSwitching(sourcesTab);
});