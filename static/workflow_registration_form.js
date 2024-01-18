import {
    apiSpecificationUrlInput,
    badApiInteractionMethodModifiedEvent,
    validateOpenApiSpecificationUrl,
} from "/static/api_specification_validation.js"

window.addEventListener("load", event => {
    validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.trim().length === 0) {
        return document.dispatchEvent(badApiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});