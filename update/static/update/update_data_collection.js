import {
    startOpenApiSpecificationUrlValidation,
    apiExecutionMethodCheckbox,
    toggleApiSpecificationUrlTextInput,
} from "/static/api_specification_validation.js";

// register-dc-script
window.addEventListener("load", async event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        startOpenApiSpecificationUrlValidation();
    }
});