import {
    isEachFileValid
} from "/static/file_upload.js";
import {
    startOpenApiSpecificationUrlValidation
} from "/static/api_specification_validation.js";

const apiExecutionMethodCheckbox = document.querySelector('input[type="checkbox"][name="interaction_methods"][value="api"]');
const apiSpecificationUrlTextInput = document.querySelector("#id_api_specification_url");

function toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox) {
    if (apiExecutionMethodCheckbox.checked) {
        apiSpecificationUrlTextInput.disabled = false;
        apiSpecificationUrlTextInput.required = true;
    } else {
        apiSpecificationUrlTextInput.disabled = true;
        apiSpecificationUrlTextInput.required = false;
    }
}

apiExecutionMethodCheckbox.addEventListener("change", event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        startOpenApiSpecificationUrlValidation();
    } else {
        document.querySelector("button[type='submit']").disabled = !isEachFileValid;
    }
});

// register-dc-script
window.addEventListener("load", async event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        startOpenApiSpecificationUrlValidation();
    }
});