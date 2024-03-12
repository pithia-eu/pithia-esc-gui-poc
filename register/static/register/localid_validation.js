const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);
const localIdTakenElement = document.querySelector(".local-id-input-group .taken-localid");
const localIdSuggestionElement = document.querySelector(".local-id-input-group .localid-suggestion");

async function checkLocalIdIsUnique(localId) {
    const response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
        localid: localId
    }));
    const responseBody = await response.json();
    return responseBody;
}

export async function validateLocalIdAndProcessResults(localIdBase, localIdSuffix, localIdSuffixInput, localIdInputGroup) {
    const localIdResponse = await checkLocalIdIsUnique(localIdBase + "_" + localIdSuffix);
    const isLocalIdUnique = localIdResponse.result;

    if (!isLocalIdUnique) {
        localIdInputGroup.classList.add("was-validated");
        localIdSuffixInput.classList.add("is-invalid");   
        if ("suggestion" in localIdResponse) {
            const suggestionSuffix = localIdResponse.suggestion.split("_").slice(1).join("_");
            localIdSuffixInput.value = suggestionSuffix;
            localIdTakenElement.innerHTML = localIdSuffix;
            localIdSuggestionElement.innerHTML = suggestionSuffix;
        }
    } else {
        localIdSuffixInput.classList.remove("is-invalid");
    }
}