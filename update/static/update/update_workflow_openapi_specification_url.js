import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    isApiSpecificationLinkValid,
    setSubmitButton,
    validateOpenApiSpecificationUrl,
} from "/static/validation/api_specification_validation.js"

window.addEventListener("load", async () => {
    setSubmitButton(document.querySelector("#workflow-openapi-spec-url-update-form button[type='submit']"));
    await validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async () => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    await validateOpenApiSpecificationUrl();
});

document.addEventListener("apiInteractionMethodModified", () => {
    enableSubmitButtonIfReady();
});

export function enableSubmitButtonIfReady() {
    document.querySelector("#workflow-openapi-spec-url-update-form button[type='submit']").disabled = !isApiSpecificationLinkValid;
}