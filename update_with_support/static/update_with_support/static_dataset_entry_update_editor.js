import {
    StaticDatasetEntryEditor,
} from "/static/metadata_editor/static_dataset_entry_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


window.addEventListener("load", async () => {
    const editor = await setupEditor(StaticDatasetEntryEditor);
});