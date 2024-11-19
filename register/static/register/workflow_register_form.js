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
import {
    startWorkflowMetadataFileValidationProcess,
} from "/static/validation/inline_workflow_validation.js";

const fileInput = document.querySelector("#id_files");
const submitButton = document.querySelector("#file-upload-form button[type=submit]");
const isWorkflowDetailsFileInputUsedCheckbox = document.querySelector("input[name='is_workflow_details_file_input_used']");
const workflowDetailsFileUploadSection = document.querySelector("#workflow_details_file_upload_section");
const workflowDetailsFileInput = document.querySelector("input[name='workflow_details_file']");
const workflowDetailsFileInputLabel = document.querySelector(`label[for="${workflowDetailsFileInput.id}"]`);

export function enableSubmitButtonIfFormIsFilledOutCorrectly() {
    if (isWorkflowDetailsFileInputUsedCheckbox.checked) {
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
    if (isWorkflowDetailsFileInputUsedCheckbox.checked) {
        workflowDetailsFileUploadSection.classList.remove("d-none");
        workflowDetailsFileInput.required = true;
        workflowDetailsFileInputLabel.classList.add("required");
        return document.dispatchEvent(new CustomEvent("workflowDetailsInputFileChanged"));
    }
    workflowDetailsFileUploadSection.classList.add("d-none");
    workflowDetailsFileInput.required = false;
    workflowDetailsFileInputLabel.classList.remove("required");
    return document.dispatchEvent(new CustomEvent("workflowDetailsInputFileChanged"));
}

function setupWorkflowDetailsFileSection() {
    updateWorkflowDetailsFileSectionState();
    isWorkflowDetailsFileInputUsedCheckbox.addEventListener("change", () => {
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

fileInput.addEventListener("change", async event => {
    await startWorkflowMetadataFileValidationProcess();
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startWorkflowMetadataFileValidationProcess();
    }
});

apiSpecificationUrlInput.addEventListener("input", async () => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    await validateOpenApiSpecificationUrl();
});