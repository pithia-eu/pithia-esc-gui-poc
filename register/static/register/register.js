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
                            <img src="/static/register/file.svg" alt="file" class="me-3">
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

async function validateXmlFileAgainstSchema(file) {
    const formData = new FormData();
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    formData.append("csrfmiddlewaretoken", csrfMiddlewareToken);
    formData.append("file", file);
    const response = await fetch(`${window.location.protocol}//${window.location.host}${window.location.pathname}validation/schema`, {
        method: "POST",
        body: formData
    });
    if (!response.ok) {
        return "error";
    }
    const isFileValid = await response.json();
    return isFileValid.result;
}

function updateXMLFileValidationStatus(state, statusElem) {
    const statusElemContent = htmlToElement(`
    <div class="d-flex">
    </div>
    `);
    if (state === "validating") {
        statusElemContent.innerHTML = `
        <div class="spinner-grow-container me-2">
            <div class="spinner-grow" style="width: 1rem; height: 1rem;" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        Validating...
        `;
        return statusElem.append(statusElemContent);
    } else if (state === "valid") {
        return statusElem.innerHTML = `Valid`;
    } else if (state === "invalid") {
        return statusElem.innerHTML = `Invalid`;
    } else if (state === "error") {
        return statusElem.innerHTML = "Encountered an error during validation.";
    }
    return statusElem.innerHTML = "Unknown";
}

async function handleFileUpload(fileInput, listElem) {
    const files = Array.from(fileInput.files);
    listUploadedFiles(files, listElem);
    const validationStatusElem = document.querySelector(".file-validation-status");
    
    for (const file of files) {
        updateXMLFileValidationStatus("validating", validationStatusElem);
        const isFileValid = await validateXmlFileAgainstSchema(file);
        if (isFileValid === "error") {
            updateXMLFileValidationStatus("error", validationStatusElem);
            continue;
        }
        updateXMLFileValidationStatus((isFileValid) ? "valid" : "invalid", validationStatusElem);
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