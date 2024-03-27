import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    inputSupportForm,
    validateAndRegister,
} from "/static/register_with_support/components/no_file_register_form.js";

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
});