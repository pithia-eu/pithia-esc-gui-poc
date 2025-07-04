import {
    ProjectEditor,
} from "/static/metadata_editor/project_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewProjectEditor extends NewRegistrationEditorMixin(ProjectEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewProjectEditor);
});