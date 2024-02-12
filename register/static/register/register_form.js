import {
    addMultipleEventListener,
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");

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