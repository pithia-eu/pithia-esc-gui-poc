import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupDataSubsetSourcesTab,
} from "/static/metadata_editor/components/data_subset/data_subset_sources_tab.js";
import {
    setupSourceFileSharingMethodSwitching,
} from "/static/metadata_editor/components/data_subset/source_file_sharing_method_switching.js";
import {
    setupTimePeriodsTab,
} from "/static/metadata_editor/components/data_subset/result_times_tab.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    DataSubsetEditorValidator,
} from "/static/metadata_editor/components/validation/data_subset_editor_validator.js";


export class DataSubsetEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        this.timePeriodsTab = setupTimePeriodsTab();
        this.sourcesTab = this.setupSourcesTab();
        setupSourceFileSharingMethodSwitching(this.sourcesTab);
    }

    getValidator() {
        return new DataSubsetEditorValidator();
    }

    setupSourcesTab() {
        return setupDataSubsetSourcesTab();
    }

    async submitAndGenerateXml() {
        this.sourcesTab.exportTabData();
        return super.submitAndGenerateXml();
    }
}