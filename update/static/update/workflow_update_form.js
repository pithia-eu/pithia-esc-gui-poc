import {
    addMultipleEventListener,
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    startMetadataFileUpdateValidationProcess,
} from "/static/validation/inline_update_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");
const fileInput = document.querySelector("#id_files");

const workflowDetailsFileExistingRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='existing']");

const workflowDetailsFileUploadRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='file_upload']");
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");

const workflowDetailsFileExternalRadioButton = document.querySelector("input[name='workflow_details_file_source'][value='external']");

const workflowDetailsFileSourceChoices = {}


function setWorkflowDetailsFileSourceChoiceState(radioButtonValue, isEnabled) {
    if ('relatedInput' in workflowDetailsFileSourceChoices[radioButtonValue]) {
        workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.disabled = !isEnabled;
        workflowDetailsFileSourceChoices[radioButtonValue].relatedInput.required = isEnabled;
    }
}

function updateWorkflowDetailsRelatedInputStates(radioButtonValue) {
    for (const key in workflowDetailsFileSourceChoices) {
        if (key != radioButtonValue) {
            setWorkflowDetailsFileSourceChoiceState(key, false);
            continue;
        }
        setWorkflowDetailsFileSourceChoiceState(key, true);
    }
}

function setupWorkflowDetailsSection() {
    // Group controls for each workflow details source choice
    if (workflowDetailsFileExistingRadioButton) {
        workflowDetailsFileSourceChoices[workflowDetailsFileExistingRadioButton.value] = {
            radioButton: workflowDetailsFileExistingRadioButton,
        }
    }
    
    workflowDetailsFileSourceChoices[workflowDetailsFileUploadRadioButton.value] = {
        radioButton: workflowDetailsFileUploadRadioButton,
        relatedInput: workflowDetailsFileInput,
    }
    workflowDetailsFileSourceChoices[workflowDetailsFileExternalRadioButton.value] = {
        radioButton: workflowDetailsFileExternalRadioButton,
    }
    const currentWorkflowDetailsSourceChoice = document.querySelector("input[name='workflow_details_file_source']:checked").value;
    updateWorkflowDetailsRelatedInputStates(currentWorkflowDetailsSourceChoice);
    for (const choice in workflowDetailsFileSourceChoices) {
        workflowDetailsFileSourceChoices[choice].radioButton.addEventListener("change", e => {
            updateWorkflowDetailsRelatedInputStates(e.target.value);
        });
    }
}

addMultipleEventListener(
    document,
    [
        "trackedFilesChanged",
        "trackedFileValidationStarted",
        "trackedFileValidationEnded",
    ],
    event => {
        const isSubmitButtonEnabled = !isEachTrackedMetadataFileValid();
        submitButton.disabled = isSubmitButtonEnabled;
    }
);

fileInput.addEventListener("change", async event => {
    await startMetadataFileUpdateValidationProcess();
});

window.addEventListener("load", async event => {
    setupWorkflowDetailsSection();
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startMetadataFileUpdateValidationProcess();
    }
});