import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCitationsTab,
} from "/static/metadata_editor/components/citations_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupKeywordsTable,
} from "/static/metadata_editor/components/project/keywords_table.js";
import {
    ProjectEditorValidator,
} from "/static/metadata_editor/components/validation/project_editor_validator.js";


export class ProjectEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        // this.keywordsTable = setupKeywordsTable();
        this.relatedPartiesTable = setupRelatedPartiesTable();
    }

    getValidator() {
        return new ProjectEditorValidator();
    }

    async submitAndGenerateXml() {
        // this.keywordsTable.exportTableDataToJsonAndStoreInOutputElement();
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}