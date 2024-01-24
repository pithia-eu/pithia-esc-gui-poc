import {
    isEachFileValid
} from "/static/file_upload.js";
import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
} from "/static/api_specification_validation.js";

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

document.addEventListener("fileValidationStatusUpdated", event => {
    enableSubmitButtonIfReady();
});

export function enableSubmitButtonIfReady() {
    if (isApiSpecificationInputAvailable) {
        document.querySelector("#file-upload-form button[type='submit']").disabled = !(isEachFileValid && isApiSpecificationLinkValid);
    } else {
        document.querySelector("#file-upload-form button[type='submit']").disabled = !isEachFileValid;
    }
}