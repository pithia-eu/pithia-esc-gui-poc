import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    OrganisationEditorValidator,
} from "/static/metadata_editor/components/validation/organisation_editor_validator.js";


export class OrganisationEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
    }

    getValidator() {
        return new OrganisationEditorValidator();
    }
}