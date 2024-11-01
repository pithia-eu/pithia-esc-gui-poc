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

export function enableSubmitButtonIfFormIsFilledOutCorrectly() {
    let isSubmitButtonEnabled = !(isEachTrackedMetadataFileValid() && isApiSpecificationLinkValid);

    return submitButton.disabled = isSubmitButtonEnabled;
}

function setupWorkflowDetailsFileSection() {
    const workflowDetailsFileUploadCheckbox = document.querySelector("input[name='is_details_file_upload_needed']");
    const workflowDetailsFileUploadSection = document.querySelector("#details_file_section");
    workflowDetailsFileUploadCheckbox.addEventListener("change", e => {
        if (workflowDetailsFileUploadCheckbox.checked) {
            return workflowDetailsFileUploadSection.classList.remove("d-none");
        }
        return workflowDetailsFileUploadSection.classList.add("d-none");
    });
}

addMultipleEventListener(
    document,
    [
        "trackedFilesChanged",
        "trackedFileValidationStarted",
        "trackedFileValidationEnded",
        "apiInteractionMethodModified",
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