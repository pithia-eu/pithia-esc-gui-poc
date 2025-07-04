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
    setupPlatformStandardIdentifiersTable,
} from "/static/metadata_editor/components/platform/platform_standard_identifiers_table.js";


export class PlatformEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupCitationsTab();
        setupGeometryLocationSection();
        this.relatedPartiesTable = setupRelatedPartiesTable();
        this.platformStandardIdentifiersTable = setupPlatformStandardIdentifiersTable();
    }

    async submitAndGenerateXml() {
        this.relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
        this.platformStandardIdentifiersTable.exportTableDataToJsonAndStoreInOutputElement();
        return super.submitAndGenerateXml();
    }
}