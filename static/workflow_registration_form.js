import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    setSubmitButton,
    validateOpenApiSpecificationUrl,
} from "/static/api_specification_validation.js"

window.addEventListener("load", event => {
    setSubmitButton(document.querySelector("#file-upload-form button[type='submit']"));
    validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});