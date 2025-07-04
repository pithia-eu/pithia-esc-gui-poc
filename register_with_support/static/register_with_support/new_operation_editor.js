import {
    OperationEditor,
} from "/static/metadata_editor/operation_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewOperationEditor extends NewRegistrationEditorMixin(OperationEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewOperationEditor);
});