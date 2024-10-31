import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";

const workflowDetailsFileUploadRadioButton = document.querySelector("input[name='workflow_details_file_format'][value='file_upload']");
const workflowDetailsFileUploadRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsFileUploadRadioButton.id}']`);
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");

const workflowDetailsFileLinkRadioButton = document.querySelector("input[name='workflow_details_file_format'][value='link']");
const workflowDetailsFileLinkRadioButtonLabel = document.querySelector(`label[for='${workflowDetailsFileLinkRadioButton.id}']`);
const workflowDetailsFileLinkTextInput = document.querySelector("input[name='workflow_details']");

const workflowDetailsRadioButtons = [
    workflowDetailsFileUploadRadioButton,
    workflowDetailsFileLinkRadioButton
];


function updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
    const isFileUploadSelected = radioButtonValue == 'file_upload';
    if (isFileUploadSelected) {
        workflowDetailsFileUploadRadioButtonLabel.classList.add("required");
        workflowDetailsFileLinkRadioButtonLabel.classList.remove("required");
    } else {
        workflowDetailsFileUploadRadioButtonLabel.classList.remove("required");
        workflowDetailsFileLinkRadioButtonLabel.classList.add("required");
    }
    workflowDetailsFileInput.disabled = !isFileUploadSelected;
    workflowDetailsFileInput.required = isFileUploadSelected;
    workflowDetailsFileLinkTextInput.disabled = isFileUploadSelected;
    workflowDetailsFileLinkTextInput.required = !isFileUploadSelected;
}

function setupWorkflowDetailsSection() {
    const currentWorkflowDetailsSharingMethodChoice = document.querySelector("input[name='workflow_details_file_format']:checked").value;
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