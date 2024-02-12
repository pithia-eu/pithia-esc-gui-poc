import {
    addMultipleEventListener,
    isEachTrackedMetadataFileValid,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
} from "/static/validation/api_specification_validation.js";

const submitButton = document.querySelector("#file-upload-form button[type=submit]");

function enableSubmitButtonIfFormIsFilledOutCorrectly() {
    let isSubmitButtonEnabled = !isEachTrackedMetadataFileValid();

    if (isApiSpecificationInputAvailable) {
        isSubmitButtonEnabled = !(isEachTrackedMetadataFileValid() && isApiSpecificationLinkValid);
    }

    return submitButton.disabled = isSubmitButtonEnabled;
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