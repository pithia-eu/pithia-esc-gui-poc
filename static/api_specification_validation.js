const apiSpecificationUrlInput = document.getElementById("id_api_specification_url");
const validationStatusList = document.querySelector(".api-specification-url-status-validation");
const apiSpecificationValidationUrl = JSON.parse(document.getElementById("api-specification-validation-url").textContent);

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.length === 0) {
        return isValidationStatusListVisibile(false);
    }

    try {
        isValidationStatusListVisibile(true);
        displayValidLinkResult(isValidOpenAPISpecificationUrl(url));
    } catch (e) {
        console.log(e);
        isValidationStatusListVisibile(true);
        displayValidLinkResult(false);
    }
});

function isValidationStatusListVisibile(isVisible) {
    if (isVisible) {
        return validationStatusList.classList.remove("d-none");
    }
    return validationStatusList.classList.add("d-none");
}

function displayValidLinkResult(isLinkValid) {
    if (isLinkValid) {
        document.querySelector(".status-invalid-link").classList.add("d-none");
        document.querySelector(".status-valid-link").classList.remove("d-none");
    } else {
        document.querySelector(".status-invalid-link").classList.remove("d-none");
        document.querySelector(".status-valid-link").classList.add("d-none");
    }
}

async function isValidOpenAPISpecificationUrl(url) {
    const formData = new FormData();
    formData.append("api_specification_url", url)
    response = await fetch(apiSpecificationValidationUrl, {
        method: "POST",
        body: formData
    });
    return JSON.parse(response).is_valid;
}