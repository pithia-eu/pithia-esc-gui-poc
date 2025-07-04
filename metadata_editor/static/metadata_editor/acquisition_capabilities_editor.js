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
    setupInstrumentModePairSection,
} from "/static/metadata_editor/components/acquisition_capabilities/instrument_mode_pair_section.js";
import {
    setupInputDescriptionsTable,
} from "/static/metadata_editor/components/acquisition_capabilities/input_descriptions_table.js";


export class AcquisitionCapabilitiesEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        setupInputDescriptionsTable();
        setupCapabilitiesTab();
        setupInstrumentModePairSection();
        setupQualityAssessmentSection();
        this.relatedPartiesTable = setupRelatedPartiesTable();
    }

    async submitAndGenerateXml() {
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}