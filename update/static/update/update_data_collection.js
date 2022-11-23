import {
    validateOpenApiSpecificationUrl,
    apiExecutionMethodCheckbox,
    toggleApiSpecificationUrlTextInput,
    toggleApiDescriptionTextarea,
} from "/static/api_specification_validation.js";

// register-dc-script
window.addEventListener("load", async event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    toggleApiDescriptionTextarea(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        validateOpenApiSpecificationUrl();
    }
});