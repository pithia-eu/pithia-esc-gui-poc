import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
    apiExecutionMethodCheckbox,
} from "/static/api_specification_validation.js";

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

function enableSubmitButtonIfReady() {
    let submitButton = document.querySelector("#file-upload-form button[type='submit']");
    if (!submitButton) {
        submitButton = document.querySelector("#interaction-methods-form button[type='submit']");
    }

    if (isApiSpecificationInputAvailable && apiExecutionMethodCheckbox.checked) {
        return submitButton.disabled = !isApiSpecificationLinkValid;
    }
    return submitButton.disabled = false;
}