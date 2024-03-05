const shortNameInput = document.querySelector("input[name='short_name']");
const localIdInputGroup = document.querySelector(".local-id-input-group");
const localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);

async function checkLocalIdIsUnique(localId) {
    console.log('localId', localId);
    const response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
        localid: localId
    }));
    const responseBody = await response.json();
    return responseBody.result;
}

shortNameInput.addEventListener("input", async () => {
    const shortName = shortNameInput.value;
    const localIdSuffix = shortName.toUpperCase().replace(/\s/g, "");
    const localIdSuffixInput = document.querySelector("input[name='localid']");
    localIdSuffixInput.value = localIdSuffix;
    const isLocalIdUnique = await checkLocalIdIsUnique(localIdBase + "_" + localIdSuffix);
    if (!isLocalIdUnique) {
        localIdInputGroup.classList.add('.was-validated');
        localIdSuffixInput.classList.add('is-invalid');
    } else {
        localIdSuffixInput.classList.remove('is-invalid');
    }
});