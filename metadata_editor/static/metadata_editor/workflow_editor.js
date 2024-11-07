import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const workflowDetailsDataHubRadioButton = document.querySelector("input[name='workflow_details_file_storage_method'][value='datahub']");
const workflowDetailsDataHubRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsDataHubRadioButton.id}']`);
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");

const workflowDetailsFileExternalRadioButton = document.querySelector("input[name='workflow_details_file_storage_method'][value='external']");
const workflowDetailsFileExternalRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsFileExternalRadioButton.id}']`);
const workflowDetailsFileExternalTextInput = document.querySelector("input[name='workflow_details']");

const workflowDetailsRadioButtons = [
    workflowDetailsDataHubRadioButton,
    workflowDetailsFileExternalRadioButton
];


function updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
    const isFileUploadSelected = radioButtonValue == workflowDetailsDataHubRadioButton.value;
    if (isFileUploadSelected) {
        workflowDetailsDataHubRadioButtonLabel.classList.add("required");
        workflowDetailsFileExternalRadioButtonLabel.classList.remove("required");
    } else {
        workflowDetailsDataHubRadioButtonLabel.classList.remove("required");
        workflowDetailsFileExternalRadioButtonLabel.classList.add("required");
    }
    workflowDetailsFileInput.disabled = !isFileUploadSelected;
    workflowDetailsFileInput.required = isFileUploadSelected;
    workflowDetailsFileExternalTextInput.disabled = isFileUploadSelected;
    workflowDetailsFileExternalTextInput.required = !isFileUploadSelected;
}

function setupWorkflowDetailsSection() {
    const currentWorkflowDetailsSharingMethodChoice = document.querySelector("input[name='workflow_details_file_storage_method']:checked").value;
    updateWorkflowDetailsRelatedInputStates(currentWorkflowDetailsSharingMethodChoice);
    workflowDetailsRadioButtons.forEach(radioButton => {
        radioButton.addEventListener("change", e => {
            updateWorkflowDetailsRelatedInputStates(e.target.value);
        });
    });
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupWorkflowDetailsSection();
});