import {
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    startMetadataFileUpdateValidationProcess,
} from "/static/validation/inline_update_file_validation.js";

const submitBtn = document.querySelector("#file-upload-form button[type=submit]");

document.addEventListener("trackedfileschanged", event => {
    const isSubmitBtnEnabled = !isEachTrackedMetadataFileValid();
    submitBtn.disabled = isSubmitBtnEnabled;
});

fileInput.addEventListener("change", async event => {
    await startMetadataFileUpdateValidationProcess();
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startMetadataFileUpdateValidationProcess();
    }
});