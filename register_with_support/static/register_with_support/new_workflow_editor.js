import {
    WorkflowEditor,
} from "/static/metadata_editor/workflow_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";
import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js";


class NewWorkflowEditor extends WorkflowEditor {
    setupEventListeners() {
        super.setupEventListeners();

        apiSpecificationUrlInput.addEventListener("input", async () => {
            const url = apiSpecificationUrlInput.value;
            if (url.trim().length === 0) {
                return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
            }
            await validateOpenApiSpecificationUrl();
        });
    }

    async runPostSetupActions() {
        await super.runPostSetupActions();
        await validateOpenApiSpecificationUrl();
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewWorkflowEditor);
});