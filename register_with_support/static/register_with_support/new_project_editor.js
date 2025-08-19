import {
    ProjectEditor,
} from "/static/metadata_editor/project_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


class NewProjectEditor extends NewRegistrationEditorMixin(ProjectEditor) {
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
    const editor = await setupEditor(NewProjectEditor);
});