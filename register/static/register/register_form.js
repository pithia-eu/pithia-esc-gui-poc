import {
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");

document.addEventListener("trackedfileschanged", event => {
    const isSubmitButtonEnabled = !isEachTrackedMetadataFileValid();
    submitButton.disabled = isSubmitButtonEnabled;
});