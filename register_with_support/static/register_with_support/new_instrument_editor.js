import {
    InstrumentEditor,
} from "/static/metadata_editor/instrument_editor.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


class NewInstrumentEditor extends NewRegistrationEditorMixin(InstrumentEditor) {
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
    const editor = await setupEditor(NewInstrumentEditor);
});