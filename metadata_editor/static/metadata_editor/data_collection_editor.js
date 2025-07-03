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


class DataCollectionEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupRelatedPartiesTable();
        setupQualityAssessmentSection();
        this.sourcesTab = setupSourcesTab();
    }

    async submitAndGenerateXml() {
        this.sourcesTab.exportTabData();
        return super.submitAndGenerateXml();
    }
}

window.addEventListener("load", () => {
    const editor = new DataCollectionEditor();
});