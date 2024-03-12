import {
    validateLocalIdAndProcessResults,
} from "/static/register/localid_validation.js";
import {
    enableLocalIdAndNamespaceFields,
    inputSupportForm,
    validateAndRegister,
} from "/static/register/no_file_register_form.js";

const nameInput = document.querySelector("input[name='name']");
const organisationInput = document.querySelector("select[name='organisation']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const organisationShortNames = JSON.parse(document.getElementById("organisation-short-names").textContent);
const namespaceInput = document.querySelector("input[name='namespace']");
const localIdSuffixInput = document.querySelector("input[name='localid']");

// Utility function
function titleCaseString(inputString) {
    const inputStringSplit = inputString.split(" ");
    for (let i = 0; i < inputStringSplit.length; i++) {
        inputStringSplit[i] = inputStringSplit[i].charAt(0).toUpperCase() + inputStringSplit[i].slice(1);
    }
    return inputStringSplit.join(" ");
}

function generateLocalId(name) {
    return titleCaseString(name).replace(/\s/g, "_");
}

nameInput.addEventListener("input", async () => {
    const localIdSuffix = generateLocalId(nameInput.value);
    localIdSuffixInput.value = localIdSuffix;

    await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
});

organisationInput.addEventListener("input", () => {
    const organisation = organisationInput.value;
    namespaceInput.value = organisationShortNames[organisation].toLowerCase().replace(/\s/g, "");
});

window.addEventListener("load", async () => {
    if (nameInput.value !== "") {
        const localIdSuffix = generateLocalId(nameInput.value);
        localIdSuffixInput.value = localIdSuffix;

        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
    }
});

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    // Enable required disabled inputs
    enableLocalIdAndNamespaceFields();

    validateAndRegister();
});