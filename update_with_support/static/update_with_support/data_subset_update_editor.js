import {
    setupDataSubsetUpdateSourcesTab,
} from "/static/update_with_support/components/data_subset/data_subset_update_sources_tab.js";
import {
    DataSubsetEditor,
} from "/static/metadata_editor/data_subset_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


class DataSubsetUpdateEditor extends DataSubsetEditor {
    setupSourcesTab() {
        return setupDataSubsetUpdateSourcesTab();
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(DataSubsetUpdateEditor);
});