import {
    IndividualEditor,
} from "/static/metadata_editor/individual_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewIndividualEditor extends NewRegistrationEditorMixin(IndividualEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewIndividualEditor);
});