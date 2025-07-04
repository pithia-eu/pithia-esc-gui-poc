import {
    AcquisitionCapabilitiesEditor,
} from "/static/metadata_editor/acquisition_capabilities_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


class NewAcquisitionCapabilitiesEditor extends NewRegistrationEditorMixin(AcquisitionCapabilitiesEditor) {
    async runAfterInitialEditorSetup() {
        await Promise.all([
            super.runAfterInitialEditorSetup(),
            this.setupNewRegistrationEditingFunctionalities(),
        ]);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewAcquisitionCapabilitiesEditor);
});