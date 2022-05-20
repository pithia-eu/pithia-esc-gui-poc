// Source for htmlToElement function: https://stackoverflow.com/a/35385518
function htmlToElement(html) {
    const template = document.createElement("template");
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

function listUploadedFiles(files, listElem) {
    listElem.innerHTML = "";
    files.forEach((file, i) => {
        listElem.append(htmlToElement(
            `<li class="list-group-item">
                <div class="row g-lg-4 g-sm-2 py-2">
                    <div class="col-lg-12">
                        <div class="file-validation-status">
                        </div>
                        <div class="file-validation-error mt-4">
                        </div>
                    </div>
                </div>
            </li>`
        ));
    });
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
            error_details: response.error.extra_details,
        };
    }
    return {
        state: state
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
            <span class="text-muted">Validating...</span>
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
    errorMsgElem.innerHTML = `
        <div class="alert alert-danger">
            Error: ${errorMsg}
        </div>
    `;
}

async function handleFileUpload(fileInput, listElem) {
    const files = Array.from(fileInput.files);
    listUploadedFiles(files, listElem);
    const validationStatusElem = document.querySelector(".file-validation-status");
    const validationStatusErrorElem = document.querySelector(".file-validation-error");
    
    for (const file of files) {
        updateXMLFileValidationStatus({ state: xmlValidationStates.VALIDATING }, validationStatusElem);
        const validationResults = await validateXmlFile(file);
        updateXMLFileValidationStatus(validationResults, validationStatusElem);
        if (validationResults.error) {
            updateXMLFileValidationErrorDetails(validationResults.error, validationStatusErrorElem);
        }
        if (validationResults.extra_details) {
            
        }
    }
}

const fileInput = document.getElementById("id_file");
const uploadedFilesList = document.querySelector(".list-uploaded-files");

fileInput.addEventListener("change", async event => {
    await handleFileUpload(fileInput, uploadedFilesList);
});

document.getElementById("register-script").addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await handleFileUpload(fileInput, uploadedFilesList);
    }
});