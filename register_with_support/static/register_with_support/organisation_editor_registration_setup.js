import {
    cleanLocalId,
} from "/static/metadata_editor/components/localid_generation.js";
import {
    validateLocalIdAndProcessResults,
} from "/static/metadata_editor/components/localid_validation.js";

const shortNameInput = document.querySelector("input[name='short_name']");
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
    window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));

    await validateLocalIdAndProcessResults(localIdBase, localIdSuffix);
});

window.addEventListener("load", async () => {
    if (shortNameInput.value !== "") {
        const localIdSuffix = generateLocalId(shortNameInput.value);
        localIdSuffixInput.value = localIdSuffix;

        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix);
    }
});