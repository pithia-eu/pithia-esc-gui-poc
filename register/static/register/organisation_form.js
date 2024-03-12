import {
    validateLocalIdAndProcessResults,
} from "/static/register/localid_validation.js";
import {
    disableLocalIdAndNamespaceFields,
    inputSupportForm,
    validateAndRegister,
} from "/static/register/no_file_register_form.js";

const shortNameInput = document.querySelector("input[name='short_name']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const localIdSuffixInput = document.querySelector("input[name='localid']");

function generateLocalId(shortName) {
    return shortName.toUpperCase().replace(/\s/g, "");
}

shortNameInput.addEventListener("input", async () => {
    const localIdSuffix = generateLocalId(shortNameInput.value);
    localIdSuffixInput.value = localIdSuffix;

    await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
});

window.addEventListener("load", async () => {
    if (shortNameInput.value !== "") {
        const localIdSuffix = generateLocalId(shortNameInput.value);
        localIdSuffixInput.value = localIdSuffix;

        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
    }
});

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    const inputs = Array.from(inputSupportForm.querySelectorAll("input"));
    const selectMenus = Array.from(inputSupportForm.querySelectorAll("select"));
    const formControls = inputs.concat(selectMenus);

    if (formControls.every(fc => fc.checkValidity())) {
        // Enable required disabled inputs
        disableLocalIdAndNamespaceFields(false);
    
        validateAndRegister();
    }
});