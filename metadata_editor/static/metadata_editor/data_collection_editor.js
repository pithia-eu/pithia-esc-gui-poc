import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupQualityAssessmentSection,
} from "/static/metadata_editor/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupSourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    DataCollectionEditorValidator,
} from "/static/metadata_editor/components/validation/data_collection_editor_validator.js";


export class DataCollectionEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupRelatedPartiesTable();
        setupQualityAssessmentSection();
        this.sourcesTab = setupSourcesTab();
    }

    getValidator() {
        return new DataCollectionEditorValidator();
    }

    async submitAndGenerateXml() {
        this.sourcesTab.exportTabData();
        return super.submitAndGenerateXml();
    }
}