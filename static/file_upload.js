export let isEachFileValid = false; // Variable is exported to work with the API specification URL input
const fileValidationStatusUpdatedEvent = new Event("fileValidationStatusUpdated");

// Source for htmlToElement() function: https://stackoverflow.com/a/35385518
function htmlToElement(html) {
    const template = document.createElement("template");
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

// Source for removeFileFromFileList() function: https://stackoverflow.com/a/64019766
function removeFileFromFileList(index, fileInput) {
    const dt = new DataTransfer();
    const { files } = fileInput;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (index !== i) {
            dt.items.add(file);
        }
    }

    fileInput.files = dt.files; // Assign the newly constructed file list
    return fileInput.files.length;
}

function resetFileValidationList(listElem) {
    listElem.innerHTML = "";
}

function loadFileValidationElemsForFile(file, listElem, index) {
    return listElem.append(htmlToElement(`
        <li class="list-group-item file-list-group-item-${index} pb-3">
            <div class="row g-2">
                <div class="col-lg-10">
                    <div class="row g-2">
                        <div class="col-lg-12 text-truncate">${file.name}</div>
                        <input type="hidden" id="is-file-${index}-valid" class="is-file-valid-status" value="false">
                        <div class="col-lg-12 file-validation-status file-validation-status-${index} text-break">
                        </div>
                        <div class="col-lg-12 file-validation-warnings file-validation-warnings-${index} text-break d-none">
                            <ul class="list-group list-group-warning">
                            </ul>
                        </div>
                        <div class="col-lg-12 file-validation-error file-validation-error-${index} text-break d-none">
                        </div>
                    </div>
                </div>
                <div class="col-lg-2">
                    <div class="d-flex flex-column justify-content-center align-items-end h-100">
                        <button id="btn-rm-file-${index}" class="btn btn-danger btn-sm btn-rm-file" data-list-item-num="${index}" type="button">Remove</button>
                    </div>
                </div>
            </div>
        </li>
    `));
}

const xmlValidationStates =  {
    VALIDATING: "validating",
    VALID: "valid",
    INVALID_SEMANTICS: "<class 'lxml.etree.DocumentInvalid'>",
    INVALID_SYNTAX: "<class 'lxml.etree.XMLSyntaxError'>",
    SUBMITTED_METADATA_NOT_MATCHING_TYPE: "<class 'validation.errors.InvalidRootElementName'>",
    INVALID_RESOURCE_URLS: "<class 'validation.errors.InvalidResourceURL'>",
    UNREGISTERED_REFERENCED_RESOURCES: "<class 'validation.errors.UnregisteredResourceReferenced'>",
    UNREGISTERED_REFERENCED_ONTOLOGY_TERMS: "<class 'validation.errors.UnregisteredOntologyTermReferenced'>",
}

async function validateXmlFile(file, fileValidationUrl, validateNotAlreadyRegistered, validateUpdatedXmlIsValid) {
    const formData = new FormData();
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    formData.append("csrfmiddlewaretoken", csrfMiddlewareToken);
    formData.append("file", file);
    if (validateNotAlreadyRegistered === true) {
        formData.append("validate_is_not_registered", true);
    }
    if (validateUpdatedXmlIsValid === true) {
        formData.append("validate_xml_file_localid_matches_existing_resource_localid", true);
        formData.append("resource_id", JSON.parse(document.getElementById("resource-id").textContent));
    }
    const response = await fetch(fileValidationUrl, {
        method: "POST",
        body: formData
    });
    let responseContent = undefined;
    try {
        responseContent = await response.json();
    } catch (error) {
        console.log(response);
        console.log(error);
        return {
            state: 'error',
            error: error,
            warnings: []
        };
    }
    if (!response.ok) {
        return {
            state: 'error',
            error: responseContent.error,
            warnings: responseContent.warnings,
        };
    }
    return {
        state: responseContent.result
    };
}

function updateXMLFileValidationStatus(fileValidationStatus, statusElem, validatingStatusMsg) {
    const statusElemContent = htmlToElement(`
        <div class="d-flex align-items-center">
        </div>
    `);
    if (fileValidationStatus.error) {
        statusElemContent.innerHTML = `
            <img src="/static/register/cross.svg" alt="cross" class="me-3"><span class="text-danger">${fileValidationStatus.error.message}</span>
        `;
    } else if (fileValidationStatus.state === "validating") {
        statusElemContent.innerHTML = `
            <div class="spinner-grow-container text-muted me-3">
                <div class="spinner-grow" style="width: 1rem; height: 1rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <span class="text-muted">${validatingStatusMsg}</span>
        `;
    } else if (fileValidationStatus.state === xmlValidationStates.VALID) {
        statusElemContent.innerHTML = `
            <img src="/static/register/tick.svg" alt="tick" class="me-3"><span class="text-success">Valid</span>
        `;
    }
    
    statusElem.innerHTML = "";
    return statusElem.append(statusElemContent);
}

function updateXMLFileValidationErrorDetails(errorMsg, errorMsgElem) {
    return errorMsgElem.innerHTML = `
        <div class="alert alert-danger mb-0" role="alert">
            ${errorMsg}
        </div>
    `;
}
function updateXMLFileValidationWarningDetails(warnings, warningListElem) {
    warnings.forEach(warning => {
        warningListElem.append(htmlToElement(`
            <li class="list-group-item list-group-item-warning">
                ${warning.details}
            </li>
        `));
    });
}

function removeClassNameFromElem(elem, className) {
    return elem.classList.remove(className);
}

const uploadFormSubmitButton = document.querySelector("form button[type='submit']");
export async function handleFileUpload(fileInput, listElem, validateNotAlreadyRegistered, validateUpdatedXmlIsValid) {
    if (!validateNotAlreadyRegistered) {
        validateNotAlreadyRegistered = false
    }
    if (!validateUpdatedXmlIsValid) {
        validateUpdatedXmlIsValid = false
    }
    resetFileValidationList(listElem);
    const btnRmFileIdsToClick = [];
    const finishedValidating = [];

    function updateIsEachFileValid(finishedValidating) {
        const numValidFiles = document.querySelectorAll(`input[class="is-file-valid-status"][value="true"]`).length;
        return isEachFileValid = numValidFiles === fileInput.files.length && finishedValidating.length === fileInput.files.length && fileInput.files.length > 0;
    }

    const files = Array.from(fileInput.files);
    files.forEach(async (file, i) => {
        loadFileValidationElemsForFile(file, listElem, i);
        const validationStatusElem = document.querySelector(`.file-validation-status-${i}`);
        const validationStatusWarningsElem = document.querySelector(`.file-validation-warnings-${i}`);
        const validationStatusWarningListElem = document.querySelector(`.file-validation-warnings-${i} .list-group-warning`);
        const validationStatusErrorElem = document.querySelector(`.file-validation-error-${i}`);
        const btnRemoveFile = document.querySelector(`#btn-rm-file-${i}`);
        btnRemoveFile.addEventListener("click", event => {
            const allBtnRmFiles = Array.from(document.querySelectorAll(".btn-rm-file"));
            const clickedBtnRmFileIndex = allBtnRmFiles.findIndex(btn => btn.id === event.target.id);
            const numFilesRemaining = removeFileFromFileList(clickedBtnRmFileIndex, fileInput);
            const listItemNum = event.target.dataset.listItemNum;
            document.querySelector(`.file-list-group-item-${listItemNum}`).remove();
            btnRmFileIdsToClick.splice(btnRmFileIdsToClick.indexOf(event.target.id), 1);
            finishedValidating.splice(finishedValidating.indexOf(`file${i}`), 1);
            updateIsEachFileValid(finishedValidating);
            document.dispatchEvent(fileValidationStatusUpdatedEvent);
        });
        uploadFormSubmitButton.disabled = true;
        updateXMLFileValidationStatus({ state: xmlValidationStates.VALIDATING }, validationStatusElem, `Validating ${file.name}`);
        let fileValidationUrl = '';
        try {
            fileValidationUrl = JSON.parse(document.getElementById("validation-url").textContent);
        } catch (error) {
            console.log(error);
        }
        const validationResults = await validateXmlFile(file, fileValidationUrl, validateNotAlreadyRegistered, validateUpdatedXmlIsValid);
        if (document.querySelector(`.file-list-group-item-${i}`)) {
            finishedValidating.push(`file${i}`);
        }
        updateXMLFileValidationStatus(validationResults, validationStatusElem);
        if (!validationResults.error) {
            document.querySelector(`input[id="is-file-${i}-valid"]`).value = "true";
            updateIsEachFileValid(finishedValidating);
            document.dispatchEvent(fileValidationStatusUpdatedEvent);
        }
        if (validationResults.warnings && document.querySelector(`.file-list-group-item-${i}`)) {
            removeClassNameFromElem(validationStatusWarningsElem, "d-none");
            updateXMLFileValidationWarningDetails(validationResults.warnings, validationStatusWarningListElem);
        }
        if (validationResults.error && document.querySelector(`.file-list-group-item-${i}`)) {
            uploadFormSubmitButton.disabled = true;
            btnRmFileIdsToClick.push(`btn-rm-file-${i}`);
            removeClassNameFromElem(validationStatusErrorElem, "d-none");
            updateXMLFileValidationErrorDetails(validationResults.error.details, validationStatusErrorElem);
        }
    });
}