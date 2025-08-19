import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    IndividualEditorValidator,
} from "/static/metadata_editor/components/validation/individual_editor_validator.js";


export class IndividualEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
    }
    
    getValidator() {
        return new IndividualEditorValidator();
    }
}