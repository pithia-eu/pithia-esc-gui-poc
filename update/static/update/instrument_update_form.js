import {
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    startInstrumentMetadataFileUpdateValidationProcess,
} from "/static/validation/inline_instrument_update_validation.js";

const fileInput = document.querySelector("#id_files");
const submitButton = document.querySelector("#file-upload-form button[type=submit]");

document.addEventListener("trackedfileschanged", event => {
    const isSubmitButtonEnabled = !isEachTrackedMetadataFileValid();
    submitButton.disabled = isSubmitButtonEnabled;
});

fileInput.addEventListener("change", async event => {
    await startInstrumentMetadataFileUpdateValidationProcess();
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startInstrumentMetadataFileUpdateValidationProcess();
    }
});