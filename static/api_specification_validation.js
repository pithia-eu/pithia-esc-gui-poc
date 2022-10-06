const apiSpecificationUrlInput = document.getElementById("id_api_specification_url");
const validationStatusList = document.querySelector('.api-specification-url-status-validation');

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.length === 0) {
        return isValidationStatusListVisibile(false);
    }

    try {
        const response = await fetch(url);
        const responseText = await response.text();
        isValidationStatusListVisibile(true);
        displayJSONValidationResult(isValidJSON(responseText));
        displayYAMLValidationResult(isValidYAML(responseText));
    } catch (e) {
        console.log(e);
        isValidationStatusListVisibile(true);
        displayJSONValidationResult(false);
        displayYAMLValidationResult(false);
    }
});

function isValidationStatusListVisibile(isVisible) {
    if (isVisible) {
        return validationStatusList.classList.remove("d-none");
    }
    return validationStatusList.classList.add("d-none");
}

function displayInvalidLinkResult(isLinkValid) {
    if (isLinkValid) {

    } else {
        
    }
}

function displayJSONValidationResult(isValid) {
    if (isValid) {
        document.querySelector(".status-invalid-json").classList.add("d-none");
        document.querySelector(".status-valid-json").classList.remove("d-none");
    } else {
        document.querySelector(".status-invalid-json").classList.remove("d-none");
        document.querySelector(".status-valid-json").classList.add("d-none");
    }
}

function displayYAMLValidationResult(isValid) {
    if (isValid) {
        document.querySelector(".status-invalid-yaml").classList.add("d-none");
        document.querySelector(".status-valid-yaml").classList.remove("d-none");
    } else {
        document.querySelector(".status-invalid-yaml").classList.remove("d-none");
        document.querySelector(".status-valid-yaml").classList.add("d-none");
    }
}

function isValidYAML(value) {
    try {
        jsyaml.load(value);
        return true;
    } catch (e) {
        console.log(e);
        return false;
    }
}

function isValidJSON(value) {
    try {
        JSON.parse(value);
        return true;
    } catch (e) {
        console.log(e);
        return false;
    }
}