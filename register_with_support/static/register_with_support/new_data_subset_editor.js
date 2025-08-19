import {
    DataSubsetEditor,
} from "/static/metadata_editor/data_subset_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


class NewDataSubsetEditor extends NewRegistrationEditorMixin(DataSubsetEditor) {
    setupEventListeners() {
        super.setupEventListeners();
        this.setupLocalIdAndNamespaceRelatedEventListeners();
    }

    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.validateLocalIdAfterInitialEditorSetupIfNeeded(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewDataSubsetEditor);
});