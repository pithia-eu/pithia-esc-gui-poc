import {
    apiSpecificationUrlInput,
} from "/static/validation/api_specification_validation.js"

export const apiExecutionMethodCheckbox = document.querySelector('input[type="checkbox"][name="api_selected"]');
export const apiSpecificationDescriptionTextarea = document.querySelector("#id_api_description");

window.addEventListener("load", () => {
    apiExecutionMethodCheckbox.disabled = true;
    apiSpecificationUrlInput.disabled = true;
    apiSpecificationDescriptionTextarea.disabled = true;
});