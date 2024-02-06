import {
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";

const submitBtn = document.querySelector("#file-upload-form button[type=submit]");

document.addEventListener("trackedfileschanged", event => {
    const isSubmitBtnEnabled = !isEachTrackedMetadataFileValid();
    submitBtn.disabled = isSubmitBtnEnabled;
});