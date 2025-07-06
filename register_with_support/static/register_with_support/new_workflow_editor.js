import {
    WorkflowEditor,
} from "/static/metadata_editor/workflow_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";
import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js";


class NewWorkflowEditor extends NewRegistrationEditorMixin(WorkflowEditor) {
    setupEventListeners() {
        super.setupEventListeners();

        this.setupLocalIdAndNamespaceRelatedEventListeners();

        apiSpecificationUrlInput.addEventListener("input", async () => {
            const url = apiSpecificationUrlInput.value;
            if (url.trim().length === 0) {
                return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
            }
            await validateOpenApiSpecificationUrl();
        });
    }

    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.validateLocalIdAfterInitialEditorSetupIfNeeded(),
            validateOpenApiSpecificationUrl(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewWorkflowEditor);
});