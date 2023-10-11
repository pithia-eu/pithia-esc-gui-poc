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
        <li class="list-group-item file-list-group-item-${index} p-4">
            <div class="d-flex align-items-md-center align-items-start">
                <div class="d-flex flex-column flex-grow-1 me-auto pe-md-5 pe-3">
                    <div class="pb-3">
                        <div class="d-flex align-items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-xml flex-shrink-0 me-3" viewBox="0 0 16 16" style="width: 1.2rem; height: 1.2rem;">
                                <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2v-1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.527 11.85h-.893l-.823 1.439h-.036L.943 11.85H.012l1.227 1.983L0 15.85h.861l.853-1.415h.035l.85 1.415h.908l-1.254-1.992 1.274-2.007Zm.954 3.999v-2.66h.038l.952 2.159h.516l.946-2.16h.038v2.661h.715V11.85h-.8l-1.14 2.596h-.025L4.58 11.85h-.806v3.999h.706Zm4.71-.674h1.696v.674H8.4V11.85h.791v3.325Z"/>
                            </svg>
                            <span class="text-break">${file.name}</span>
                        </div>
                    </div>
                    <div class="d-flex flex-column" style="row-gap: 1rem;">
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
                <button id="btn-rm-file-${index}" class="btn btn-outline-dark btn-sm btn-rm-file" data-list-item-num="${index}" type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill pe-none" viewBox="0 0 16 16">
                        <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
                    </svg>
                </button>
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
    let jsonParseError = undefined;
    try {
        responseContent = await response.json();
    } catch (error) {
        console.log("response", response);
        console.log(error);
        jsonParseError = error;
    }
    if (!response.ok) {
        return {
            state: "error",
            error: (responseContent === undefined ? {
                message: "An error occurred whilst checking the validation results.",
                details: jsonParseError
            } : responseContent.error),
            warnings: (responseContent === undefined ? [] : responseContent.warnings),
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
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill text-danger flex-shrink-0 me-3" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
        </svg>
        <span class="text-danger">${fileValidationStatus.error.message}</span>
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
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2 text-success flex-shrink-0 me-3" viewBox="0 0 16 16" style="height: 1.5rem; width: 1.5rem;">
            <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
        </svg>
        <span class="text-success">Valid</span>
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