const nameInput = document.querySelector("input[name='name']");
const organisationInput = document.querySelector("select[name='organisation']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);
const organisationShortNames = JSON.parse(document.getElementById("organisation-short-names").textContent);
const namespaceInput = document.querySelector("input[name='namespace']");

async function checkLocalIdIsUnique(localId) {
    const response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
        localid: localId
    }));
    const responseBody = await response.json();
    return responseBody.result;
}

// Utility function
function titleCaseString(inputString) {
    const inputStringSplit = inputString.split(" ");
    for (let i = 0; i < inputStringSplit.length; i++) {
        inputStringSplit[i] = inputStringSplit[i].charAt(0).toUpperCase() + inputStringSplit[i].slice(1);
    }
    return inputStringSplit.join(" ");
}

nameInput.addEventListener("input", async () => {
    const name = nameInput.value;
    const localIdSuffix = titleCaseString(name).replace(/\s/g, "_");
    const localIdSuffixInput = document.querySelector("input[name='localid']");
    localIdSuffixInput.value = localIdSuffix;
    const isLocalIdUnique = await checkLocalIdIsUnique(localIdBase + "_" + localIdSuffix);
    if (!isLocalIdUnique) {
        localIdInputGroup.classList.add(".was-validated");
        localIdSuffixInput.classList.add("is-invalid");
    } else {
        localIdSuffixInput.classList.remove("is-invalid");
    }
});

organisationInput.addEventListener("input", () => {
    const organisation = organisationInput.value;
    namespaceInput.value = organisationShortNames[organisation].toLowerCase().replace(/\s/g, "");
});