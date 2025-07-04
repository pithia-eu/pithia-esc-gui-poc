import {
    DataSubsetEditor,
} from "/static/metadata_editor/data_subset_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewDataSubsetEditor extends NewRegistrationEditorMixin(DataSubsetEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewDataSubsetEditor);
});