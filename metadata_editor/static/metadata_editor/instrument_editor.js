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
    setupOperationalModesTable,
} from "/static/metadata_editor/components/instrument/operational_modes_table.js";


export class InstrumentEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        this.relatedPartiesTable = setupRelatedPartiesTable();
        this.operationalModesTable = setupOperationalModesTable();
    }

    async submitAndGenerateXml() {
        this.operationalModesTable.exportTableDataToJsonAndStoreInOutputElement();
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}