import {
    ProcessEditor,
} from "/static/metadata_editor/process_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewProcessEditor extends NewRegistrationEditorMixin(ProcessEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewProcessEditor);
});