import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
} from "/static/api_specification_validation.js";
import {
    apiExecutionMethodCheckbox,
} from "/static/interaction_methods_form.js";
let submitButton;

window.addEventListener("load", () => {
    submitButton = document.querySelector("#file-upload-form button[type='submit']");
    if (submitButton === null) {
        submitButton = document.querySelector("#interaction-methods-form button[type='submit']")
    }
});

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

function enableSubmitButtonIfReady() {
    if (isApiSpecificationInputAvailable && apiExecutionMethodCheckbox.checked) {
        return submitButton.disabled = !isApiSpecificationLinkValid;
    }
    return submitButton.disabled = false;
}