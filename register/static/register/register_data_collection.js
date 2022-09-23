const apiExecutionMethodCheckbox = document.querySelector('input[type="checkbox"][name="execution_methods"][value="api"]');
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
});

// register-dc-script
window.addEventListener("load", async event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
});