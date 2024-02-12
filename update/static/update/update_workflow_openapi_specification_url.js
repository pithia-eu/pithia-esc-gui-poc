import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    isApiSpecificationLinkValid,
    setSubmitButton,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js"

window.addEventListener("load", event => {
    setSubmitButton(document.querySelector("#workflow-openapi-spec-url-update-form button[type='submit']"));
    validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});

document.addEventListener("apiInteractionMethodModified", event => {
    enableSubmitButtonIfReady();
});

export function enableSubmitButtonIfReady() {
    document.querySelector("#workflow-openapi-spec-url-update-form button[type='submit']").disabled = !isApiSpecificationLinkValid;
}