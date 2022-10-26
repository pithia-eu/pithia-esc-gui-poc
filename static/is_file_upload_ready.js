import {
    isEachFileValid
} from "/static/file_upload.js";
import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
    apiExecutionMethodCheckbox,
} from "/static/api_specification_validation.js";

export function enableSubmitButtonIfReady() {
    let isFileReadyToSubmit = isEachFileValid;
    if (isApiSpecificationInputAvailable) {
        if (apiExecutionMethodCheckbox.checked) {
            isFileReadyToSubmit = isEachFileValid && isApiSpecificationLinkValid;
        }
    }
    document.querySelector("button[type='submit']").disabled = !isFileReadyToSubmit;
}