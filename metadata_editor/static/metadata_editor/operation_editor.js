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
    setupGeometryLocationSection,
} from "/static/metadata_editor/components/geometry_location_section.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupOperationTimeSection,
} from "/static/metadata_editor/components/operation/operation_time_section.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";


export class OperationEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        setupGeometryLocationSection();
        setupOperationTimeSection();
        setupTimePeriodElements(
            "input[name='time_instant_begin_position']",
            "input[name='time_instant_end_position']"
        );
        this.relatedPartiesTable = setupRelatedPartiesTable();
    }

    async submitAndGenerateXml() {
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}