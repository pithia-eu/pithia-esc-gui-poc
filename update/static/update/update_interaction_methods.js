import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
} from "/static/api_specification_validation.js";
import {
    apiExecutionMethodCheckbox,
} from "/static/interaction_methods_form.js";

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