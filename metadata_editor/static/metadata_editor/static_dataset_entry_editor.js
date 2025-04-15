import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const staticDatasetCategorySelect = document.querySelector("select[name='static_dataset_category']");
const nameInputHelpText = document.querySelector("input[name='name'] + .form-text");


function updateNameInputHelpText() {
    const selectedStaticDatasetCategoryOption = staticDatasetCategorySelect.options[staticDatasetCategorySelect.selectedIndex];
    const staticDatasetCategoryUrl = selectedStaticDatasetCategoryOption.value;
    let staticDatasetCategory = selectedStaticDatasetCategoryOption.text;
    if (!staticDatasetCategoryUrl) {
        return nameInputHelpText.classList.add("d-none");
    }
    if (staticDatasetCategoryUrl === "https://metadata.pithia.eu/ontology/2.2/staticDatasetCategory/TrainingDataset") {
        staticDatasetCategory = "Training Dataset";
    }
    nameInputHelpText.textContent = `The name of the ${staticDatasetCategory}`;
    return nameInputHelpText.classList.remove("d-none");
}

staticDatasetCategorySelect.addEventListener("change", updateNameInputHelpText);

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    updateNameInputHelpText();
    setupWizardManualAndAutoSave();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
});