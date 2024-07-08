import {
    generateLocalId,
} from "/static/metadata_editor/components/localid_generation.js";

const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);
const invalidFeedbackElement = document.querySelector(".local-id-input-group .invalid-feedback");

const nameInput = document.querySelector("input[name='name']");
const organisationInput = document.querySelector("select[name='organisation']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const namespacesByOrganisation = JSON.parse(document.getElementById("namespaces-by-organisation").textContent);
const namespaceInput = document.querySelector("input[name='namespace']");
const localIdSuffixInput = document.querySelector("input[name='localid']");

async function checkLocalIdIsUnique(localId) {
    let localIdCheck = {};
    if (!localIdValidationUrl || localIdValidationUrl.length === 0) {
        const msg = "Cannot check local ID as no validation URL supplied.";
        console.log(msg);
        localIdCheck.error = msg;
        localIdCheck.displayError = true;
        return localIdCheck;
    }

    let response;
    try {
        response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
            localid: localId
        }));
        const responseBody = await response.json();
        localIdCheck = {
            ...localIdCheck,
            ...responseBody,
        };
    } catch (error) {
        const msg = "Encountered an error checking local ID for uniqueness.";
        console.error(error);
        console.log(msg);
        if (response) console.error(`Response:`, response);
        localIdCheck.error = `${msg} Please try again later.`;
        localIdCheck.displayError = true;
    }
    return localIdCheck;
}

export async function setupLocalIdAndNamespaceRelatedEventListeners() {
    if (nameInput.value !== "") {
        const localIdSuffix = generateLocalId(nameInput.value);
        localIdSuffixInput.value = localIdSuffix;

        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix);
    }

    nameInput.addEventListener("input", async () => {
        const localIdSuffix = generateLocalId(nameInput.value);
        localIdSuffixInput.value = localIdSuffix;
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    
        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix);
    });
    
    organisationInput.addEventListener("input", () => {
        const organisation = organisationInput.value;
        if (organisation === "") {
            return namespaceInput.value = "";
        }
        namespaceInput.value = namespacesByOrganisation[organisation].toLowerCase().replace(/\s/g, "");
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    });
}

function displayLocalIdError(error) {
    localIdInputGroup.classList.add("was-validated");
    localIdSuffixInput.classList.add("is-invalid");
    invalidFeedbackElement.textContent = error;
}

function displayLocalIdSuggestion(localIdCheck, localIdSuffix) {
    if (!("suggestion" in localIdCheck)) {
        return displayLocalIdError(`Local ID with suffix "${localIdSuffix}" has been taken. An alternative cannot be suggested at this time. Please try generating another local ID.`);
    }
    const suggestionSuffix = localIdCheck.suggestion.split("_").slice(1).join("_");
    localIdSuffixInput.value = suggestionSuffix;
    return displayLocalIdError(`Local ID with suffix "${localIdSuffix}" is already in use so "${suggestionSuffix}" will be used instead.`);
}

export async function validateLocalIdAndProcessResults(localIdBase, localIdSuffix) {
    const localIdCheck = await checkLocalIdIsUnique(localIdBase + "_" + localIdSuffix);
    if ("error" in localIdCheck) {
        if ("displayError" in localIdCheck) displayLocalIdError(localIdCheck.error);
        return;
    }
    const isLocalIdInUse = localIdCheck.result;

    if (isLocalIdInUse) {
        displayLocalIdSuggestion(localIdCheck, localIdSuffix);
    } else {
        localIdSuffixInput.classList.remove("is-invalid");
    }
    window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
}