export let isApiSpecificationLinkValid = false;
export let isApiSpecificationInputAvailable = false;
export const apiExecutionMethodCheckbox = document.querySelector('input[type="checkbox"][name="api_selected"]');
export const apiSpecificationUrlInput = document.querySelector("#id_api_specification_url");
export const apiSpecificationDescriptionTextarea = document.querySelector("#id_api_description");
const validationStatusList = document.querySelector(".api-specification-url-status-validation");
const apiSpecificationValidationUrl = JSON.parse(document.getElementById("api-specification-validation-url").textContent);
let userInputTimeout;
const apiInteractionMethodModifiedEvent = new Event("apiInteractionMethodModified");

export function toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox) {
    if (apiExecutionMethodCheckbox.checked) {
        apiSpecificationUrlInput.disabled = false;
        apiSpecificationUrlInput.required = true;
    } else {
        apiSpecificationUrlInput.disabled = true;
        apiSpecificationUrlInput.required = false;
    }
}

export function toggleApiDescriptionTextarea(apiExecutionMethodCheckbox) {
    if (apiExecutionMethodCheckbox.checked) {
        apiSpecificationDescriptionTextarea.disabled = false;
        apiSpecificationDescriptionTextarea.required = true;
    } else {
        apiSpecificationDescriptionTextarea.disabled = true;
        apiSpecificationDescriptionTextarea.required = false;
    }
}

export function validateOpenApiSpecificationUrl() {
    const url = apiSpecificationUrlInput.value;
    if (url.length === 0) {
        isApiSpecificationLinkValid = false;
        isValidationStatusListVisibile(false);
        document.dispatchEvent(apiInteractionMethodModifiedEvent);
        return;
    }

    document.querySelector("button[type='submit']").disabled = true;
    displayValidatingSpinner(true);
    if (userInputTimeout !== undefined) {
        clearTimeout(userInputTimeout);
    }
    userInputTimeout = setTimeout(async () => {
        try {
            const validationResult = await sendOpenApiSpecificationUrlForValidation(url);
            const { valid, error, details } = validationResult;
            isApiSpecificationLinkValid = valid;
            if (apiSpecificationUrlInput.value.length === 0) {
                isApiSpecificationLinkValid = false;
                displayValidLinkResult(isApiSpecificationLinkValid);
            }
            displayValidLinkResult(validationResult);
            document.dispatchEvent(apiInteractionMethodModifiedEvent);
        } catch (e) {
            console.log(e);
            displayValidLinkResult(false);
        }
    }, 500);
}

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

async function sendOpenApiSpecificationUrlForValidation(url) {
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

window.addEventListener("load", event => {
    isApiSpecificationInputAvailable = true;
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    toggleApiDescriptionTextarea(apiExecutionMethodCheckbox);
    if (apiExecutionMethodCheckbox.checked) {
        validateOpenApiSpecificationUrl();
    }
});

apiExecutionMethodCheckbox.addEventListener("change", event => {
    toggleApiSpecificationUrlTextInput(apiExecutionMethodCheckbox);
    toggleApiDescriptionTextarea(apiExecutionMethodCheckbox);
    if (!apiExecutionMethodCheckbox.checked) {
        return document.dispatchEvent(apiInteractionMethodModifiedEvent);
    }
    isApiSpecificationLinkValid = false;
    document.dispatchEvent(apiInteractionMethodModifiedEvent);
    validateOpenApiSpecificationUrl();
});

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (apiExecutionMethodCheckbox.checked && url.trim().length === 0) {
        isApiSpecificationLinkValid = false;
        return document.dispatchEvent(apiInteractionMethodModifiedEvent);
    }
    validateOpenApiSpecificationUrl();
});