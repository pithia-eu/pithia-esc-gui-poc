import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    isApiSpecificationLinkValid,
    setSubmitButton,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js";
import {
    addMultipleEventListener,
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");
const workflowDetailsFileDataHubStorageMethodRadioButton = document.querySelector("input[name='details_file_storage_method'][value='datahub']");
const workflowDetailsFileExternalStorageMethodRadioButton = document.querySelector("input[name='details_file_storage_method'][value='external']");
const workflowDetailsFileUploadSection = document.querySelector("#details_file_upload_section");
const workflowDetailsFileInput = document.querySelector("input[name='details_file']");

export function enableSubmitButtonIfFormIsFilledOutCorrectly() {
    if (workflowDetailsFileDataHubStorageMethodRadioButton.checked) {
        return submitButton.disabled = !(
            isEachTrackedMetadataFileValid()
            && isApiSpecificationLinkValid
            && workflowDetailsFileInput.value
        );
    }

    return submitButton.disabled = !(
        isEachTrackedMetadataFileValid()
        && isApiSpecificationLinkValid
    );
}

function updateWorkflowDetailsFileSectionState() {
    if (workflowDetailsFileDataHubStorageMethodRadioButton.checked) {
        workflowDetailsFileUploadSection.classList.remove("d-none");
        return document.dispatchEvent(new CustomEvent("workflowDetailsInputFileChanged"));
    }
    workflowDetailsFileUploadSection.classList.add("d-none");
    return document.dispatchEvent(new CustomEvent("workflowDetailsInputFileChanged"));
}

function setupWorkflowDetailsFileSection() {
    updateWorkflowDetailsFileSectionState();
    workflowDetailsFileDataHubStorageMethodRadioButton.addEventListener("input", e => {
        updateWorkflowDetailsFileSectionState();
    });
    workflowDetailsFileExternalStorageMethodRadioButton.addEventListener("input", e => {
        updateWorkflowDetailsFileSectionState();
    });
    workflowDetailsFileInput.addEventListener("input", e => {
        document.dispatchEvent(new CustomEvent("workflowDetailsInputFileChanged"));
    });
}

addMultipleEventListener(
    document,
    [
        "trackedFilesChanged",
        "trackedFileValidationStarted",
        "trackedFileValidationEnded",
        "apiInteractionMethodModified",
        "workflowDetailsInputFileChanged",
    ],
    event => {
        enableSubmitButtonIfFormIsFilledOutCorrectly();
    }
);

window.addEventListener("load", async () => {
    setSubmitButton(document.querySelector("#file-upload-form button[type='submit']"));
    setupWorkflowDetailsFileSection();
    await validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async () => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    await validateOpenApiSpecificationUrl();
});