const parser = new DOMParser();
const expectedRootElementName = JSON.parse(document.querySelector("#expected-root-element-name").textContent);

// Events
const trackedFilesChangedEvent = new Event("trackedfileschanged");

// Error messages
const COULD_NOT_CHECK_ERROR = "Could not check as syntax is invalid.";

const trackedMetadataFiles = [];

export class MetadataFile {
    constructor(xmlFileString, xmlFileName) {
        this.id = Math.ceil(Math.random()*10000);
        this.xmlFileString = xmlFileString;
        this.name = xmlFileName;
        this.xmlDoc = this.parseXmlString(xmlFileString);
        this.syntaxErrors = undefined;
        this.namespaceErrors = undefined;
        this.localIDErrors = undefined;
        this.rootElementNameErrors = undefined;
        this.XSDErrors = undefined;
        this.metadataReferenceErrors = undefined;
        this.ontologyReferenceErrors = undefined;
    }

    static async fromFile(xmlFile) {
        const xmlFileString = await xmlFile.text();
        return new MetadataFile(xmlFileString, xmlFile.name);
    }

    get isSyntaxValid() {
        if (this.syntaxErrors === undefined) {
            return false;
        }
        return this.syntaxErrors.length === 0;
    }

    get isNamespaceValid() {
        if (this.namespaceErrors === undefined) {
            return false;
        }
        return this.namespaceErrors.length === 0;
    }

    get isLocalIDValid() {
        if (this.localIDErrors === undefined) {
            return false;
        }
        return this.localIDErrors.length === 0;
    }

    get isRootElementNameValid() {
        if (this.rootElementNameErrors === undefined) {
            return false;
        }
        return this.rootElementNameErrors.length === 0;
    }

    get isXSDValid() {
        if (this.XSDErrors === undefined) {
            return false;
        }
        return this.XSDErrors.length === 0;
    }

    get isEachMetadataReferenceValid() {
        if (this.metadataReferenceErrors === undefined) {
            return false;
        }
        return this.metadataReferenceErrors.length === 0;
    }

    get isEachOntologyReferenceValid() {
        if (this.ontologyReferenceErrors === undefined) {
            return false;
        }
        return this.ontologyReferenceErrors.length === 0;
    }

    get isValid() {
        return [
            this.isSyntaxValid,
            this.isNamespaceValid,
            this.isLocalIDValid,
            this.isRootElementNameValid,
            this.isXSDValid,
            this.isEachMetadataReferenceValid,
            this.isEachOntologyReferenceValid,
        ].every(result => result === true);
    }

    get totalErrorCount() {
        return [
            this.syntaxErrors,
            this.namespaceErrors,
            this.localIDErrors,
            this.rootElementNameErrors,
            this.XSDErrors ? this.XSDErrors : [],
            this.metadataReferenceErrors ? this.metadataReferenceErrors : [],
            this.ontologyReferenceErrors ? this.ontologyReferenceErrors : [],
        ].flat().length;
    }

    addBasicValidationResults(results) {
        this.syntaxErrors = results.syntaxErrors;
        this.namespaceErrors = results.namespaceErrors;
        this.localIDErrors = results.localIDErrors;
        this.rootElementNameErrors = results.rootElementNameErrors;
    }

    addReferenceValidationResults(results) {
        this.metadataReferenceErrors = results.metadataReferenceErrors;
        this.ontologyReferenceErrors = results.ontologyReferenceErrors;
    }

    addServerValidationResults(results) {
        // Implemented through subclasses
    }

    addXsdValidationResults(results) {
        this.XSDErrors = results.XSDErrors;
    }

    parseXmlString(xmlString) {
        return parser.parseFromString(xmlString, "application/xml");
    }
}

export class MetadataFileValidator {
    removeFileExtensionFromString(string) {
        return string.replace(/\.[^/.]+$/, "")
    }

    validateSyntax(xmlDoc) {
        const errors = [];
        const errorNode = xmlDoc.querySelector("parsererror");
        if (errorNode !== null) {
            try {
                const errorDetails = errorNode.querySelector("h3 + div").textContent;
                errors.push(errorDetails);
            } catch (error) {
                const errorDetails = errorNode.textContent;
                errors.push(errorDetails);
            }
        }
        return errors;
    }

    validateRootElementName(xmlDoc) {
        const rootElement = xmlDoc.querySelector(":root");
        const errors = [];
        if (rootElement.nodeName !== expectedRootElementName) {
            errors.push(`Expected a root element name of "${expectedRootElementName}" but got "${rootElement.nodeName}".`)
        }
        return errors;
    }

    validateLocalID(xmlDoc, xmlFileName) {
        const localID = xmlDoc.querySelector("localID");
        const errors = [];

        // Check if localID element is present.
        if (localID === null) {
            errors.push("A localID element was not found in your metadata file.")
            return errors;
        }

        // Check if the localID is matching with the file name.
        if (localID.textContent !== this.removeFileExtensionFromString(xmlFileName)) {
            errors.push(`The localID (${localID.textContent}) must be matching the the name of the file (${xmlFileName}).`);
        }

        // Check localID content.
        const re = new RegExp("^[\\w-]+$");
        if (re.test(localID.textContent) === false) {
            errors.push("The localID can only contain alphanumeric characters with optional use of dashes and/or underscores.");
        }

        return errors;
    }

    validateNamespace(xmlDoc) {
        const namespace = xmlDoc.querySelector("namespace");
        const errors = [];

        // Check if namespace element is present.
        if (namespace === null) {
            errors.push("A namespace element was not found in your metadata file.")
            return errors;
        }

        // Check namespace content.
        const re = new RegExp("^[\\w-]+$");
        if (re.test(namespace.textContent) === false) {
            errors.push("The namespace can only contain alphanumeric characters with optional use of dashes and/or underscores.");
        }

        return errors;
    }

    validateBasicComponents(metadataFile) {
        const xmlDoc = metadataFile.xmlDoc;
        const syntaxErrors = this.validateSyntax(xmlDoc);
        const rootElementNameErrors = syntaxErrors.length > 0 ? [COULD_NOT_CHECK_ERROR] : this.validateRootElementName(xmlDoc);
        const localIDErrors = syntaxErrors.length > 0 ? [COULD_NOT_CHECK_ERROR] : this.validateLocalID(xmlDoc, metadataFile.name);
        const namespaceErrors = syntaxErrors.length > 0 ? [COULD_NOT_CHECK_ERROR] : this.validateNamespace(xmlDoc);
        
        return {
            syntaxErrors: syntaxErrors,
            rootElementNameErrors: rootElementNameErrors,
            localIDErrors: localIDErrors,
            namespaceErrors: namespaceErrors,
        }
    }

    async validateWithXsd(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline-xsd-validation-url").textContent);

        let response;
        try {
            response = await fetch(`${validationUrl}?` + new URLSearchParams({
                xml_file_string: metadataFile.xmlFileString,
            }));
        } catch (error) {
            console.error("There was a problem whilst validating with XSD.");
            const errorMsg = "A network error occurred.";
            return {
                XSDErrors: [errorMsg],
            }
        }

        if (response.status === 504) {
            const errorMsg = "Validation did not finish. The connection to the server timed out before validation could finish. Please try uploading the file again at a later time.";
            return {
                XSDErrors: [errorMsg],
            };
        }

        let responseText;
        let results;
        try {
            responseText = await response.text();
            results = JSON.parse(responseText);
        } catch (error) {
            if (!response.ok) {
                const errorMsg = "An unexpected error occurred.";
                return {
                    XSDErrors: [errorMsg],
                };
            }
        }

        return {
            XSDErrors: results.xml_file_xsd_errors
        };
    }

    async serverValidationFetchRequest(metadataFile) {
        // Implemented by subclasses
    }

    serverValidationErrorObject(errorMsg) {
        // Implemented by subclasses
    }

    serverValidationResultsObject(results) {
        // Implemented by subclasses
    }

    async validateWithServer(metadataFile) {
        let response;
        try {
            response = await this.serverValidationFetchRequest(metadataFile);
        } catch (error) {
            console.error("There was a problem whilst validating with the server.");
            const errorMsg = "A network error occurred.";
            return this.serverValidationErrorObject(errorMsg);
        }
        
        if (response.status === 504) {
            const errorMsg = "Validation did not finish. The connection to the server timed out before validation could finish. Please try uploading the file again at a later time.";
            return this.serverValidationErrorObject(errorMsg);
        }

        let responseText;
        let results;
        try {
            responseText = await response.text();
            results = JSON.parse(responseText);
        } catch (error) {
            if (!response.ok) {
                const errorMsg = "An unexpected error occurred.";
                return this.serverValidationErrorObject(errorMsg);
            }
        }

        return this.serverValidationResultsObject(results);
    }
}

export class MetadataValidationStatusUIController {
    constructor(validationStatusListElem, fileInputElem) {
        this.validationStatusListElem = validationStatusListElem;
        this.fileInputElem = fileInputElem;
    }

    htmlToElement(html) {
        const template = document.createElement("template");
        html = html.trim();
        template.innerHTML = html;
        return template.content.firstChild;
    }

    // Source for removeFileFromFileList() function: https://stackoverflow.com/a/64019766
    #removeFileFromFileList(index) {
        const dt = new DataTransfer();
        const { files } = this.fileInputElem;
    
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (index !== i) {
                dt.items.add(file);
            }
        }
    
        this.fileInputElem.files = dt.files; // Assign the newly constructed file list
        return this.fileInputElem.files.length;
    }

    #removeMetadataFileAndRemoveFromValidationStatusList(metadataFile) {
        const allBtnRmFiles = Array.from(document.querySelectorAll(".btn-rm-file"));
        const clickedBtnRmFileIndex = allBtnRmFiles.findIndex(btn => btn.id === `btn-rm-file-${metadataFile.id}`);

        // Remove file from file input based on index
        this.#removeFileFromFileList(clickedBtnRmFileIndex);

        // Remove file from UI
        document.querySelector(`.file-list-group-item-${metadataFile.id}`).remove();

        // Remove file from code store
        removeTrackedMetadataFileById(metadataFile.id);
        document.dispatchEvent(trackedFilesChangedEvent);
    }

    #addRemoveButtonForFile(metadataFile) {
        document.querySelector(`#btn-rm-file-${metadataFile.id}`).addEventListener("click", event => {
            this.#removeMetadataFileAndRemoveFromValidationStatusList(metadataFile);
        });
    }

    addSuccessValidationResultsForFile(successText, selector) {
        const statusElem = document.querySelector(selector);
        statusElem.innerHTML = `
        <div class="text-success">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
            </svg>${successText}
        </div>`;
    }

    addFailedValidationResultsForFile(failureText, errors, selector) {
        const statusElem = document.querySelector(selector);
        let errorLisString = "";
        errors.forEach(e => errorLisString += `<li>${e}</li>`);
        statusElem.innerHTML = `
        <details class="text-danger">
            <summary>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill text-danger me-2" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                </svg>${failureText}
            </summary>
            <div class="pt-2">
                <ul>
                    ${errorLisString}
                </ul>
            </div>
        </details>`;
    }

    #setFileAsValid(selector) {
        const mainStatusElem = document.querySelector(selector);
        mainStatusElem.className = "text-success";
        mainStatusElem.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
        </svg>Valid`;
    }

    #setFileAsInvalid(selector) {
        const mainStatusElem = document.querySelector(selector);
        mainStatusElem.className = "text-danger";
        mainStatusElem.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill me-2" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/>
        </svg>This metadata file did not pass all the checks.`;
    }

    #updateTotalErrorCountForFile(metadataFile) {
        const errorNumElem = document.querySelector(`.file-list-group-item-${metadataFile.id} .num-errors`);
        errorNumElem.innerHTML = metadataFile.totalErrorCount > 1 ? metadataFile.totalErrorCount + " errors" : metadataFile.totalErrorCount + " error";
    }

    addGenericListItemForMetadataFile(metadataFile) {
        this.validationStatusListElem.append(this.htmlToElement(`
            <li class="list-group-item file-list-group-item file-list-group-item-${metadataFile.id} p-4">
                <div class="d-flex flex-column flex-grow-1">
                    <div class="pb-3">
                        <div class="d-flex align-items-center w-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-xml flex-shrink-0 me-3" viewBox="0 0 16 16" style="width: 1.2rem; height: 1.2rem;">
                                <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2v-1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.527 11.85h-.893l-.823 1.439h-.036L.943 11.85H.012l1.227 1.983L0 15.85h.861l.853-1.415h.035l.85 1.415h.908l-1.254-1.992 1.274-2.007Zm.954 3.999v-2.66h.038l.952 2.159h.516l.946-2.16h.038v2.661h.715V11.85h-.8l-1.14 2.596h-.025L4.58 11.85h-.806v3.999h.706Zm4.71-.674h1.696v.674H8.4V11.85h.791v3.325Z"/>
                            </svg>
                            <span class="text-truncate me-auto">${metadataFile.name}</span>
                            <button id="btn-rm-file-${metadataFile.id}" class="btn btn-outline-dark btn-sm btn-rm-file" data-list-item-num="${metadataFile.id}" type="button">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill pe-none" viewBox="0 0 16 16">
                                    <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <details class="details-validation p-2">
                        <summary>
                            <div class="d-inline-flex flex-column row-gap-2">
                                <div class="d-inline-flex align-items-center column-gap-2">
                                    <span class="main-validation-status">
                                        <span class="text-secondary">
                                            <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                                <span class="visually-hidden">Loading...</span>
                                            </div>Validating
                                        </span>
                                    </span>
                                    <small class="text-secondary total-time-validated">
                                        (<span class="time-value">-</span>)
                                    </small>
                                </div>
                                <small class="error-counter text-danger">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill text-danger me-2" viewBox="0 0 16 16">
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                                    </svg><span class="num-errors">0 errors</span>
                                </small>
                                <small class="warning-counter">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle-fill text-warning me-2" viewBox="0 0 16 16">
                                        <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                                    </svg><span class="num-warnings">0 warnings</span>
                                </small>
                            </div>
                        </summary>
                        <ul class="list-unstyled mt-2">
                            <li class="sv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating syntax
                                </div>
                            </li>
                            <li class="renv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating type
                                </div>
                            </li>
                            <li class="liv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating local ID
                                </div>
                            </li>
                            <li class="nsv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating namespace
                                </div>
                            </li>
                            <li class="mrv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating references to other metadata
                                </div>
                            </li>
                            <li class="orv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating references to ontology references
                                </div>
                            </li>
                            <li class="xv-list-group-item py-2">
                                <div class="text-secondary">
                                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>Validating XSD
                                </div>
                            </li>
                        </ul>
                    </details>
                </div>
            </li>
        `));
    }

    addMetadataFileToValidationStatusList(metadataFile) {
        // Implemented through subclasses
    }

    startValidationForFile(metadataFile) {
        this.addMetadataFileToValidationStatusList(metadataFile);
        this.#addRemoveButtonForFile(metadataFile);
    }

    updateBasicValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const svSelector = `.sv-list-group-item`;
        const nsvSelector = `.nsv-list-group-item`;
        const livSelector = `.liv-list-group-item`;
        const renvSelector = `.renv-list-group-item`;

        // Syntax validation results
        if (metadataFile.isSyntaxValid) {
            this.addSuccessValidationResultsForFile(
                "Passed syntax validation.",
                `${fileListGroupItemSelector} ${svSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed syntax validation.",
                metadataFile.syntaxErrors,
                `${fileListGroupItemSelector} ${svSelector}`
            );
        }
        
        // Namespace validation results
        if (metadataFile.isNamespaceValid) {
            this.addSuccessValidationResultsForFile(
                "Passed namespace validation.",
                `${fileListGroupItemSelector} ${nsvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed namespace validation.",
                metadataFile.namespaceErrors,
                `${fileListGroupItemSelector} ${nsvSelector}`
            );
        }

        // Local ID validation results
        if (metadataFile.isLocalIDValid) {
            this.addSuccessValidationResultsForFile(
                "Passed local ID validation.",
                `${fileListGroupItemSelector} ${livSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed local ID validation.",
                metadataFile.localIDErrors,
                `${fileListGroupItemSelector} ${livSelector}`
            );
        }

        // Root element name validation results
        if (metadataFile.isRootElementNameValid) {
            this.addSuccessValidationResultsForFile(
                "Passed type validation.",
                `${fileListGroupItemSelector} ${renvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed type validation.",
                metadataFile.rootElementNameErrors,
                `${fileListGroupItemSelector} ${renvSelector}`
            );
        }

        this.#updateTotalErrorCountForFile(metadataFile);
    }

    updateReferenceValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const mrvSelector = `.mrv-list-group-item`;
        const orvSelector = `.orv-list-group-item`;

        // Metadata reference validation results
        if (metadataFile.isEachMetadataReferenceValid) {
            this.addSuccessValidationResultsForFile(
                "Passed metadata reference validation.",
                `${fileListGroupItemSelector} ${mrvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed metadata reference validation.",
                metadataFile.metadataReferenceErrors,
                `${fileListGroupItemSelector} ${mrvSelector}`
            );
        }
        
        // Ontology reference validation results
        if (metadataFile.isEachOntologyReferenceValid) {
            this.addSuccessValidationResultsForFile(
                "Passed ontology reference validation.",
                `${fileListGroupItemSelector} ${orvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed ontology reference validation.",
                metadataFile.ontologyReferenceErrors,
                `${fileListGroupItemSelector} ${orvSelector}`
            );
        }

        this.#updateTotalErrorCountForFile(metadataFile);
    }

    updateServerValidationResultsForFile(metadataFile) {
        // Implemented through subclasses
    }

    updateXsdValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const xvSelector = `.xv-list-group-item`;

        // Metadata reference validation results
        if (metadataFile.isXSDValid) {
            this.addSuccessValidationResultsForFile(
                "Passed XSD validation.",
                `${fileListGroupItemSelector} ${xvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed XSD validation.",
                metadataFile.XSDErrors,
                `${fileListGroupItemSelector} ${xvSelector}`
            );
        }

        this.#updateTotalErrorCountForFile(metadataFile);
    }

    endValidationForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        document.querySelector(fileListGroupItemSelector).classList.add("finished");
        const mainSummarySelector = ".details-validation > summary .main-validation-status";
        if (metadataFile.isValid) {
            return this.#setFileAsValid(`${fileListGroupItemSelector} ${mainSummarySelector}`);
        }
        return this.#setFileAsInvalid(`${fileListGroupItemSelector} ${mainSummarySelector}`);
    }

    updateTimeTakenToValidateFile(metadataFile, startTime, endTime) {
        const timeValueElem = document.querySelector(`.file-list-group-item-${metadataFile.id} .total-time-validated .time-value`);
        // Convert start and end time difference to seconds 
        const timeValue = (endTime - startTime) / 1000;
        if (timeValue < 1) {
            timeValueElem.innerHTML = "Less than a second";
        } else if (timeValue < 59.5) {
            // 59.5 as Math.round() rounds up if more than 59.5.
            timeValueElem.innerHTML = `${Math.round(timeValue)}s`;
        } else {
            // If equal to or over 60s, convert to mins and secs
            timeValueElem.innerHTML = `${parseInt(timeValue / 60)}m ${Math.round((timeValue % 60))}s`;
        }
    }
}

export async function validateMetadataFile(metadataFile, validator, validationStatusUIController) {
    try {
        const validationStartTime = new Date().getTime();
        validationStatusUIController.startValidationForFile(metadataFile);
    
        const basicValidationResults = validator.validateBasicComponents(metadataFile);
        metadataFile.addBasicValidationResults(basicValidationResults);
        validationStatusUIController.updateBasicValidationResultsForFile(metadataFile);
    
        const serverValidationResults = metadataFile.isSyntaxValid ? await validator.validateWithServer(metadataFile) : validator.serverValidationErrorObject(COULD_NOT_CHECK_ERROR);
        metadataFile.addServerValidationResults(serverValidationResults);
        validationStatusUIController.updateServerValidationResultsForFile(metadataFile);
    
        const XsdValidationResults = metadataFile.isSyntaxValid ? await validator.validateWithXsd(metadataFile) : {
            XSDErrors: [COULD_NOT_CHECK_ERROR],
        };
        metadataFile.addXsdValidationResults(XsdValidationResults);
        validationStatusUIController.updateXsdValidationResultsForFile(metadataFile);
    
        validationStatusUIController.endValidationForFile(metadataFile);
        const validationEndTime = new Date().getTime();
    
        validationStatusUIController.updateTimeTakenToValidateFile(metadataFile, validationStartTime, validationEndTime);
    } catch (error) {
        console.log(`Validation process for metadata file ${metadataFile.id} did not run to completion. It may have been removed from the file list.`);
        console.error(error);
    }
}

export async function startValidationProcess(files, validator, validationStatusUIController, newMetadataFileObjectFn) {
    const validationRequests = [];

    for (const file of files) {
        const metadataFile = await newMetadataFileObjectFn(file);
        addTrackedMetadataFile(metadataFile);
        validationRequests.push(validateMetadataFile(metadataFile, validator, validationStatusUIController));
    };

    await Promise.all(validationRequests);
    document.dispatchEvent(trackedFilesChangedEvent);
}

export function addTrackedMetadataFile(metadataFile) {
    return trackedMetadataFiles.push(metadataFile);
}

function removeTrackedMetadataFileById(metadataFileId) {
    const metadataFileIndex = trackedMetadataFiles.findIndex(metadataFile => metadataFile.id === metadataFileId);
    return trackedMetadataFiles.splice(metadataFileIndex, 1);
}

export function isEachTrackedMetadataFileValid() {
    return trackedMetadataFiles.every(metadataFile => metadataFile.isValid === true);
}