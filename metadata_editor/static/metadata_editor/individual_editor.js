import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";


class IndividualEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
    }
    
}

window.addEventListener("load", () => {
    const editor = new IndividualEditor();
});