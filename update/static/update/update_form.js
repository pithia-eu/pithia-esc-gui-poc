import {
    addMultipleEventListener,
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    startMetadataFileUpdateValidationProcess,
} from "/static/validation/inline_update_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");
const fileInput = document.querySelector("#id_files");

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
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startMetadataFileUpdateValidationProcess();
    }
});