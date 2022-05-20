// Source for htmlToElement function: https://stackoverflow.com/a/35385518
function htmlToElement(html) {
    const template = document.createElement("template");
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

function loadFileValidationElems(file, containerElem) {
    containerElem.innerHTML = "";
    return containerElem.append(htmlToElement(`
        <div class="row g-lg-4 g-sm-2">
            <div class="col-lg-12">
                <div class="file-validation-status">
                </div>
            </div>
            <div class="col-lg-12">
                <div class="file-validation-error">
                </div>
            </div>
        </div>
    `));
}

const xmlValidationStates =  {
    VALIDATING: "validating",
    VALID: "valid",
    INVALID_SEMANTICS: "<class 'lxml.etree.DocumentInvalid'>",
    INVALID_SYNTAX: "<class 'lxml.etree.XMLSyntaxError'>",
    UNREGISTERED_XLINK_HREFS: "<class 'register.exceptions.UnregisteredXlinkHrefsException'>",
}

async function validateXmlFile(file) {
    const formData = new FormData();
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    formData.append("csrfmiddlewaretoken", csrfMiddlewareToken);
    formData.append("file", file);
    const response = await fetch(`${window.location.protocol}//${window.location.host}${window.location.pathname}validation/schema`, {
        method: "POST",
        body: formData
    });
    const responseContent = await response.json();
    if (!response.ok) {
        return {
            state: responseContent.error.type,
            error: responseContent.error.message,
            extra_details: responseContent.error.extra_details,
        };
    }
    return {
        state: responseContent.result
    };
}

function updateXMLFileValidationStatus(fileValidationStatus, statusElem) {
    const statusElemContent = htmlToElement(`
    <div class="d-flex align-items-center">
    </div>
    `);
    if (fileValidationStatus.state === "validating") {
        statusElemContent.innerHTML = `
            <div class="spinner-grow-container text-muted me-3">
                <div class="spinner-grow" style="width: 1rem; height: 1rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <span class="text-muted">Validating metadata</span>
        `;
    } else if (fileValidationStatus.state === xmlValidationStates.VALID) {
        statusElemContent.innerHTML = `
            <img src="/static/register/tick.svg" alt="tick" class="me-3"><span class="text-success">Valid</span>
        `;
    } else if (fileValidationStatus.state === xmlValidationStates.INVALID_SEMANTICS) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">XML does not conform to the corresponding schema.</span>
        `;
    } else if (fileValidationStatus.state === xmlValidationStates.INVALID_SYNTAX) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Syntax is invalid.</span>
        `;
    } else if (fileValidationStatus.state === xmlValidationStates.UNREGISTERED_XLINK_HREFS) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3">
            <span class="text-danger">
                One or multiple resources referenced by the xlink:href attribute have not been registered with the e-Science Centre.
            </span>
        `;
    } else {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Encountered an unknown error during validation.</span>
        `;
    }
    
    statusElem.innerHTML = "";
    return statusElem.append(statusElemContent);
}

function updateXMLFileValidationErrorDetails(errorMsg, errorMsgElem) {
    return errorMsgElem.innerHTML = `
        <div class="alert alert-danger mb-0" role="alert">
            Error: ${errorMsg}
        </div>
    `;
}

function appendFurtherRegistrationActionsToErrorDetails(unregisteredReferencedResourceTypes, registrationLinksElem) {
    const extraDetailsMessage = htmlToElement('<div class="mt-5">Please access the links below to register the resources referenced in the submitted metadata file:</div>');
    const registrationLinksList = htmlToElement(`<ul class="mt-2"></ul>`);
    unregisteredReferencedResourceTypes.forEach(resourceType => {
        registrationLinksList.appendChild(htmlToElement(`
            <li><a href="${window.location.protocol}//${window.location.host}/register/${resourceType}" target="_blank" class="alert-link">${resourceType.charAt(0).toUpperCase() + resourceType.slice(1)} Metadata Registration</a></li>
        `));
    });
    registrationLinksElem.append(extraDetailsMessage);
    return registrationLinksElem.append(registrationLinksList);
}

async function handleFileUpload(fileInput, containerElem) {
    const file = Array.from(fileInput.files)[0];
    loadFileValidationElems(file, containerElem);
    const validationStatusElem = document.querySelector(".file-validation-status");
    const validationStatusErrorElem = document.querySelector(".file-validation-error");
    
    updateXMLFileValidationStatus({ state: xmlValidationStates.VALIDATING }, validationStatusElem);
    const validationResults = await validateXmlFile(file);
    updateXMLFileValidationStatus(validationResults, validationStatusElem);
    if (validationResults.error) {
        updateXMLFileValidationErrorDetails(validationResults.error, validationStatusErrorElem);
    }
    if (!validationResults.extra_details) {
        return;
    }
    if (validationResults.extra_details.unregistered_referenced_resource_types) {
        const metadataRegistrationLinksElem = document.querySelector(".file-validation-error .alert");
        appendFurtherRegistrationActionsToErrorDetails(validationResults.extra_details.unregistered_referenced_resource_types, metadataRegistrationLinksElem);
    }
}

const fileInput = document.getElementById("id_file");
const fileValidationStatusElem = document.querySelector(".card-file-validation-status .file-validation-status-container");

fileInput.addEventListener("change", async event => {
    await handleFileUpload(fileInput, fileValidationStatusElem);
});

document.getElementById("register-script").addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await handleFileUpload(fileInput, fileValidationStatusElem);
    }
});