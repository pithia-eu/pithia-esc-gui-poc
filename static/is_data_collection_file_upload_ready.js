import {
    isEachFileValid
} from "/static/file_upload.js";
import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
    apiExecutionMethodCheckbox,
} from "/static/api_specification_validation.js";

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

document.addEventListener("fileValidationStatusUpdated", event => {
    enableSubmitButtonIfReady();
});

export function enableSubmitButtonIfReady() {
    if (isApiSpecificationInputAvailable) {
        document.querySelector("button[type='submit']").disabled = !(isEachFileValid && isApiSpecificationLinkValid && apiExecutionMethodCheckbox.checked);
    } else {
        document.querySelector("button[type='submit']").disabled = !isEachFileValid;
    }
}