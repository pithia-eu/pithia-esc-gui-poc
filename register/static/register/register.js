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
                    <div class="col-lg-8">
                        <div class="d-flex align-items-center">
                            <img src="/static/register/file.svg" alt="file" class="file-icon me-3">
                            <input type="hidden" name="file${i}-name" value="${file.name}">
                            <span class="file-name" title=${file.name}>${file.name}</span>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="file-validation-status">
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
    INVALID_SEMANTICS: "invalid",
    INVALID_SYNTAX: "XMLSyntaxError",
    INTERNAL_SERVER_ERROR: "InternalServerError",
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
    console.log(response.status);
    if (response.status === 422) {
        return xmlValidationStates.INVALID_SYNTAX;
    }
    if (!response.ok) {
        return xmlValidationStates.INTERNAL_SERVER_ERROR;
    }
    const responseContent = await response.json();
    const isFileValid = (responseContent.result) ? xmlValidationStates.VALID : xmlValidationStates.INVALID_SEMANTICS;
    return isFileValid;
}

function updateXMLFileValidationStatus(state, statusElem) {
    const statusElemContent = htmlToElement(`
    <div class="d-flex align-items-center">
    </div>
    `);
    if (state === "validating") {
        statusElemContent.innerHTML = `
            <div class="spinner-grow-container text-muted me-3">
                <div class="spinner-grow" style="width: 1rem; height: 1rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <span class="text-muted">Validating...</span>
        `;
    } else if (state === xmlValidationStates.VALID) {
        statusElemContent.innerHTML = `
            <img src="/static/register/tick.svg" alt="tick" class="me-3"><span class="text-success">Valid</span>
        `;
    } else if (state === xmlValidationStates.INVALID_SEMANTICS) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Semantically incorrect.</span>
        `;
    } else if (state === xmlValidationStates.INVALID_SYNTAX) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Encountered an unknown error during validation.</span>
        `;
    } else if (state === xmlValidationStates.INTERNAL_SERVER_ERROR) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Encountered an unknown error during validation.</span>
        `;
    } else {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">Unknown state.</span>
        `;
    }
    
    statusElem.innerHTML = "";
    return statusElem.append(statusElemContent);
}

async function handleFileUpload(fileInput, listElem) {
    const files = Array.from(fileInput.files);
    listUploadedFiles(files, listElem);
    const validationStatusElem = document.querySelector(".file-validation-status");
    
    for (const file of files) {
        updateXMLFileValidationStatus(xmlValidationStates.VALIDATING, validationStatusElem);
        const validationResults = await validateXmlFile(file);
        updateXMLFileValidationStatus(validationResults, validationStatusElem);
    }
}

const collapseGuidance = document.getElementById("collapse-guidance")
const bsCollapseGuidance = new bootstrap.Collapse(collapseGuidance, {
    toggle: false
});
const fileInput = document.getElementById("id_files");
const uploadedFilesList = document.querySelector(".list-uploaded-files");

fileInput.addEventListener("change", async event => {
    await handleFileUpload(fileInput, uploadedFilesList);
    bsCollapseGuidance.show();
});

document.getElementById("register-script").addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await handleFileUpload(fileInput, uploadedFilesList);
        bsCollapseGuidance.show();
    }
});