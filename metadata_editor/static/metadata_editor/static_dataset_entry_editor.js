import {
    BaseEditor,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupPhenomenonTimeSection,
} from "/static/metadata_editor/components/static_dataset_entry/phenomenon_time_section.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";


class StaticDatasetEntryEditor extends BaseEditor {
    setup() {
        super.setup();
        setupWizardManualAndAutoSave();
        setupPhenomenonTimeSection();
        setupTimePeriodElements(
            "input[name='time_instant_begin_position']",
            "input[name='time_instant_end_position']"
        );
        this.nameInputHelpText = document.querySelector("input[name='name'] + .form-text");
        this.staticDatasetCategorySelect = document.querySelector("select[name='static_dataset_category']");
        this.updateNameInputHelpText();
    }

    setupEventListeners() {
        super.setupEventListeners();
        this.staticDatasetCategorySelect.addEventListener("change", () => {
            this.updateNameInputHelpText();
        });
    }

    updateNameInputHelpText() {
        const selectedStaticDatasetCategoryOption = this.staticDatasetCategorySelect.options[this.staticDatasetCategorySelect.selectedIndex];
        const staticDatasetCategoryUrl = selectedStaticDatasetCategoryOption.value;
        let staticDatasetCategory = selectedStaticDatasetCategoryOption.text;
        if (!staticDatasetCategoryUrl) {
            return this.nameInputHelpText.classList.add("d-none");
        }
        if (staticDatasetCategoryUrl === "https://metadata.pithia.eu/ontology/2.2/staticDatasetCategory/TrainingDataset") {
            staticDatasetCategory = "Training Dataset";
        }
        this.nameInputHelpText.textContent = `The name of the ${staticDatasetCategory}`;
        return this.nameInputHelpText.classList.remove("d-none");
    }

    async submitAndGenerateXml() {
        return super.submitAndGenerateXml();
    }
}

window.addEventListener("load", () => {
    const editor = new StaticDatasetEntryEditor();
});