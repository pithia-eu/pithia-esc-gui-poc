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
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
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
    setupProcessingInputsTable,
} from "/static/metadata_editor/components/computation_capabilities/processing_inputs_table.js";


class ComputationCapabilitiesEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        setupCapabilitiesTab();
        setupQualityAssessmentSection();
        this.setupSoftwareReferenceSection();
        this.relatedPartiesTable = setupRelatedPartiesTable();
        this.processingInputsTable = setupProcessingInputsTable();
    }

    checkAndSetSoftwareReferenceConditionalRequiredFields() {
        checkAndSetRequiredAttributesForFields(
            this.softwareReferenceSectionRequiredFields,
            this.softwareReferenceSectionOptionalFields,
        );
    }
    
    setupSoftwareReferenceSection() {
        // Instantiate variables for section first
        this.softwareReferenceSection = document.querySelector("#software-reference-section");
        this.softwareReferenceSectionRequiredFields = [
            this.softwareReferenceSection.querySelector("input[name='software_reference_citation_title']"),
            this.softwareReferenceSection.querySelector("input[name='software_reference_citation_publication_date']"),
        ];
        this.softwareReferenceSectionOptionalFields = [
            this.softwareReferenceSection.querySelector("input[name='software_reference_citation_doi']"),
            this.softwareReferenceSection.querySelector("textarea[name='software_reference_other_citation_details']"),
            this.softwareReferenceSection.querySelector("input[name='software_reference_citation_linkage_url']"),
        ];

        this.checkAndSetSoftwareReferenceConditionalRequiredFields();
    
        let allSoftwareReferenceFields = [
            ...this.softwareReferenceSectionRequiredFields,
            ...this.softwareReferenceSectionOptionalFields,
        ];
        for (const field of allSoftwareReferenceFields) {
            field.addEventListener("input", () => {
                this.checkAndSetSoftwareReferenceConditionalRequiredFields();
            });
        }
    }

    async submitAndGenerateXml() {
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}

window.addEventListener("load", async () => {
    const editor = new ComputationCapabilitiesEditor();
});