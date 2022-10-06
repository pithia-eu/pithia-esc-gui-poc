const apiSpecificationUrlInput = document.getElementById("id_api_specification_url");
const validationStatusList = document.querySelector('.api-specification-url-status-validation');
const syntaxStatusElements = document.querySelectorAll(".status-syntax");

apiSpecificationUrlInput.addEventListener("input", async event => {
    const url = apiSpecificationUrlInput.value;
    if (url.length === 0) {
        return isValidationStatusListVisibile(false);
    }

    try {
        const response = await fetch(url);
        const responseText = await response.text();
        isValidationStatusListVisibile(true);
        displayValidLinkResult(true);
        displayJSONValidationResult(isValidJSON(responseText));
        displayYAMLValidationResult(isValidYAML(responseText));
    } catch (e) {
        console.log(e);
        isValidationStatusListVisibile(true);
        displayValidLinkResult(false);
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

function displayValidLinkResult(isLinkValid) {
    if (isLinkValid) {
        document.querySelector(".status-invalid-link").classList.add("d-none");
    } else {
        syntaxStatusElements.forEach(e => {
            e.classList.add("d-none");
        })
        document.querySelector(".status-invalid-link").classList.remove("d-none");
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