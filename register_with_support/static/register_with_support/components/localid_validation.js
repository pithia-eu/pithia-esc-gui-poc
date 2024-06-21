import {
    generateLocalId,
} from "/static/register_with_support/components/localid_generation.js";

const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);
const localIdTakenElement = document.querySelector(".local-id-input-group .taken-localid");
const localIdSuggestionElement = document.querySelector(".local-id-input-group .localid-suggestion");

const nameInput = document.querySelector("input[name='name']");
const organisationInput = document.querySelector("select[name='organisation']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const namespacesByOrganisation = JSON.parse(document.getElementById("namespaces-by-organisation").textContent);
const namespaceInput = document.querySelector("input[name='namespace']");
const localIdSuffixInput = document.querySelector("input[name='localid']");

async function checkLocalIdIsUnique(localId) {
    const response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
        localid: localId
    }));
    const responseBody = await response.json();
    return responseBody;
}

export function setupLocalIdAndNamespaceRelatedEventListeners() {
    nameInput.addEventListener("input", async () => {
        const localIdSuffix = generateLocalId(nameInput.value);
        localIdSuffixInput.value = localIdSuffix;
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    
        await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
    });
    
    organisationInput.addEventListener("input", () => {
        const organisation = organisationInput.value;
        if (organisation === "") {
            return namespaceInput.value = "";
        }
        namespaceInput.value = namespacesByOrganisation[organisation].toLowerCase().replace(/\s/g, "");
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    });
    
    window.addEventListener("load", async () => {
        if (nameInput.value !== "") {
            const localIdSuffix = generateLocalId(nameInput.value);
            localIdSuffixInput.value = localIdSuffix;
    
            await validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup);
        }
    });
}

export async function validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup) {
    const localIdResponse = await checkLocalIdIsUnique(localIdBase + "_" + localIdSuffix);
    const isLocalIdInUse = localIdResponse.result;

    if (isLocalIdInUse) {
        localIdInputGroup.classList.add("was-validated");
        localIdSuffixInput.classList.add("is-invalid");   
        if ("suggestion" in localIdResponse) {
            const suggestionSuffix = localIdResponse.suggestion.split("_").slice(1).join("_");
            localIdSuffixInput.value = suggestionSuffix;
            localIdTakenElement.textContent = localIdSuffix;
            localIdSuggestionElement.textContent = suggestionSuffix;
        }
    } else {
        localIdSuffixInput.classList.remove("is-invalid");
    }
    window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
}