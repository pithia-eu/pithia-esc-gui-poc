import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCapabilitiesTab,
} from "/static/metadata_editor/components/capabilities_tab.js";
import {
    setupCitationsTab,
} from "/static/metadata_editor/components/citations_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    ProcessEditorValidator,
} from "/static/metadata_editor/components/validation/process_editor_validator.js";


export class ProcessEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        setupCapabilitiesTab();
        setupQualityAssessmentSection();
        this.relatedPartiesTable = setupRelatedPartiesTable();
    }

    getValidator() {
        return new ProcessEditorValidator();
    }

    async submitAndGenerateXml() {
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}