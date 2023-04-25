import {
    isApiSpecificationInputAvailable,
    isApiSpecificationLinkValid,
    apiExecutionMethodCheckbox,
} from "/static/api_specification_validation.js";

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

function enableSubmitButtonIfReady() {
    if (isApiSpecificationInputAvailable && apiExecutionMethodCheckbox.checked) {
        return document.querySelector("button[type='submit']").disabled = !isApiSpecificationLinkValid;
    }
    return document.querySelector("button[type='submit']").disabled = false;
}