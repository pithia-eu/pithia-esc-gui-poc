const apiSpecificationUrlInput = document.getElementById("id_api_specification_url");
const validationStatusList = document.querySelector(".api-specification-url-status-validation");
const apiSpecificationValidationUrl = JSON.parse(document.getElementById("api-specification-validation-url").textContent);
let userInputTimeout;

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.length === 0) {
        return isValidationStatusListVisibile(false);
    }

    displayValidatingSpinner(true);
    if (userInputTimeout !== undefined) {
        clearTimeout(userInputTimeout);
    }
    userInputTimeout = setTimeout(async () => {
        try {
            displayValidLinkResult(await validateOpenAPISpecificationUrl(url));
        } catch (e) {
            console.log(e);
            displayValidLinkResult(false);
        }
    }, 500);
});

function isValidationStatusListVisibile(isVisible) {
    if (isVisible) {
        return validationStatusList.classList.remove("d-none");
    }
    return validationStatusList.classList.add("d-none");
}

function displayValidatingSpinner(isVisible) {
    isValidationStatusListVisibile(false);
    document.querySelector(".status-invalid-link").classList.add("d-none");
    if (isVisible === true) {
        document.querySelector(".status-validating-link").classList.remove("d-none");
    } else {
        document.querySelector(".status-validating-link").classList.add("d-none");
    }
}

function displayValidLinkResult(validationResult) {
    const { valid, error, details } = validationResult;
    isValidationStatusListVisibile(true);
    document.querySelector(".status-validating-link").classList.add("d-none");
    if (valid === true) {
        isValidationStatusListVisibile(false);
        document.querySelector(".status-invalid-link").classList.add("d-none");
    } else {
        document.querySelector(".status-invalid-link .status-details").classList.add("d-none");
        document.querySelector(".status-invalid-link").classList.remove("d-none");
        document.querySelector(".status-invalid-link .status-text").innerHTML = "An unexpected error occurred.";
        if (error) {
            document.querySelector(".status-invalid-link .status-text").innerHTML = error;
        }
        if (details) {
            document.querySelector(".status-invalid-link .status-details span").innerHTML = details;
            document.querySelector(".status-invalid-link .status-details").classList.remove("d-none");
        }
    }
}

async function validateOpenAPISpecificationUrl(url) {
    const formData = new FormData();
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    formData.append("csrfmiddlewaretoken", csrfMiddlewareToken);
    formData.append("api_specification_url", url);
    const response = await fetch(apiSpecificationValidationUrl, {
        method: "POST",
        body: formData
    });
    return await response.json();
}