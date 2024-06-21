import {
    cleanLocalId,
} from "/static/register_with_support/components/localid_generation.js";
import {
    validateLocalIdAndProcessResults,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/register_with_support/components/editor_manual_and_autosave.js";

const shortNameInput = document.querySelector("input[name='short_name']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const localIdSuffixInput = document.querySelector("input[name='localid']");

// Organisation local ID is generated using a different method
// to all other metadata types.
function generateLocalId(shortName) {
    return cleanLocalId(shortName.toUpperCase().replace(/\s/g, ""));
}

shortNameInput.addEventListener("input", async () => {
    const localIdSuffix = generateLocalId(shortNameInput.value);
    localIdSuffixInput.value = localIdSuffix;

    await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
});

window.addEventListener("load", async () => {
    setupWizardManualAndAutoSave();
    if (shortNameInput.value !== "") {
        const localIdSuffix = generateLocalId(shortNameInput.value);
        localIdSuffixInput.value = localIdSuffix;

        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
    }
});

editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    validateAndRegister();
});