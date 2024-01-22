import {
    apiInteractionMethodModifiedEvent,
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    setSubmitButton,
    validateOpenApiSpecificationUrl,
} from "/static/api_specification_validation.js"

export const apiExecutionMethodCheckbox = document.querySelector('input[type="checkbox"][name="api_selected"]');
export const apiSpecificationDescriptionTextarea = document.querySelector("#id_api_description");
let submitButton;

export function toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox) {
    if (apiExecutionMethodCheckbox.checked) {
        apiSpecificationUrlInput.disabled = false;
        apiSpecificationUrlInput.required = true;
    } else {
        apiSpecificationUrlInput.disabled = true;
        apiSpecificationUrlInput.required = false;
    }
}

export function toggleApiDescriptionTextarea(apiExecutionMethodCheckbox) {
    if (apiExecutionMethodCheckbox.checked) {
        apiSpecificationDescriptionTextarea.disabled = false;
    } else {
        apiSpecificationDescriptionTextarea.disabled = true;
    }
}

window.addEventListener("load", event => {
    submitButton = document.querySelector("#file-upload-form button[type='submit']");
    if (submitButton === null) {
        submitButton = document.querySelector("#interaction-methods-form button[type='submit']")
    }
    setSubmitButton(submitButton);
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    toggleApiDescriptionTextarea(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        validateOpenApiSpecificationUrl();
    }
});

apiExecutionMethodCheckbox.addEventListener("change", event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    toggleApiDescriptionTextarea(apiExecutionMethodCheckbox);
    if (!apiExecutionMethodCheckbox.checked) {
        return document.dispatchEvent(apiInteractionMethodModifiedEvent);
    }
    document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (apiExecutionMethodCheckbox.checked && url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});
