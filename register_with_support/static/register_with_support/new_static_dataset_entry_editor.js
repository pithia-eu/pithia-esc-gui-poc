import {
    StaticDatasetEntryEditor,
} from "/static/metadata_editor/static_dataset_entry_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewStaticDatasetEntryEditor extends NewRegistrationEditorMixin(StaticDatasetEntryEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewStaticDatasetEntryEditor);
});