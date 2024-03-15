import {
    validateLocalIdAndProcessResults,
} from "/static/register_with_support/localid_validation.js";
import {
    inputSupportForm,
    validateAndRegister,
} from "/static/register_with_support/no_file_register_form.js";

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
    validateAndRegister();
});