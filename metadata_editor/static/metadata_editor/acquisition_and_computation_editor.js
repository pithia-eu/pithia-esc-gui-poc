import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupCapabilityLinksTab,
} from "/static/metadata_editor/components/acquisition_and_computation/capability_links_tab.js";
import {
    AcquisitionAndComputationEditorValidator,
} from "/static/metadata_editor/components/validation/acquisition_and_computation_editor_validator.js";


export class AcquisitionAndComputationEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCapabilityLinksTab();
    }

    getValidator() {
        return new AcquisitionAndComputationEditorValidator();
    }
}