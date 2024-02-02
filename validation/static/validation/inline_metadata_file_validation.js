const parser = new DOMParser();
const expectedRootElementName = "Organisation";
const testXml = `<?xml version="1.0" encoding="UTF-8"?>
<Organisation 
    xmlns="https://metadata.pithia.eu/schemas/2.2" xsi:schemaLocation="https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:gmd="http://www.isotc211.org/2005/gmd"
    xmlns:gco="http://www.isotc211.org/2005/gco" >

    <identifier>
        <PITHIA_Identifier>
            <localID>Organisation_Test</localID>
            <namespace>test</namespace>
            <version>1</version>
            <creationDate>2022-02-03T12:50:00Z</creationDate>
            <lastModificationDate>2022-02-03T12:50:00Z</lastModificationDate>
        </PITHIA_Identifier>
    </identifier>
    <name>Organisation Test</name>
    <contactInfo>
        <CI_Contact xmlns="http://www.isotc211.org/2005/gmd">
            <phone>
                <CI_Telephone><voice><gco:CharacterString>+1 000-000-0000</gco:CharacterString></voice> <!-- telephone -->
                </CI_Telephone>
            </phone>           
            <address>
                <CI_Address>                   
                    <deliveryPoint><gco:CharacterString>123 Abc Street, Suite 123</gco:CharacterString></deliveryPoint> <!-- street name, number -->
                    <city><gco:CharacterString>City</gco:CharacterString></city>
                    <administrativeArea><gco:CharacterString>XY</gco:CharacterString></administrativeArea>
                    <postalCode><gco:CharacterString>00000</gco:CharacterString></postalCode>
                    <country><gco:CharacterString>Country</gco:CharacterString></country>
                    <electronicMailAddress><gco:CharacterString>test@test.edu</gco:CharacterString></electronicMailAddress>
                </CI_Address>
            </address>
            <onlineResource><CI_OnlineResource><linkage><URL>http://test.test.edu</URL></linkage></CI_OnlineResource></onlineResource> 
            <hoursOfService><gco:CharacterString>0:00am-0:00am</gco:CharacterString></hoursOfService>
            <contactInstructions><gco:CharacterString>Contact by email or phone</gco:CharacterString></contactInstructions> <!-- Supplemental instructions on how or when to contact the individual. -->
        </CI_Contact>
    </contactInfo>
    <shortName>TEST</shortName>
    <description>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
        labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </description>
</Organisation>`;
const invalidTestXml = "invalid xml";
const testFile = new File([testXml], "Organisation_Test.xml");

class MetadataFile {
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
        const xmlFileString = await testFile.text();
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

    addXsdValidationResults(results) {
        
    }

    parseXmlString(xmlString) {
        return parser.parseFromString(xmlString, "application/xml");
    }
}

class MetadataFileValidator {
    removeFileExtensionFromString(string) {
        return string.replace(/\.[^/.]+$/, "")
    }

    validateSyntax(xmlDoc) {
        const errorNode = xmlDoc.querySelector("parsererror");
        const errors = [];
        if (errorNode) {
            const errorDetails = errorNode.querySelector("h3 + div").textContent;
            errors.push(errorDetails);
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
        const rootElementNameErrors = syntaxErrors.length > 0 ? ["Could not evaluate root element name as was unable to parse XML."] : this.validateRootElementName(xmlDoc);
        const localIDErrors = this.validateLocalID(xmlDoc, metadataFile.name);
        const namespaceErrors = this.validateNamespace(xmlDoc);
        
        return {
            syntaxErrors: syntaxErrors,
            rootElementNameErrors: rootElementNameErrors,
            localIDErrors: localIDErrors,
            namespaceErrors: namespaceErrors,
        }
    }

    async validateWithXsd(metadataFile) {

    }

    async validateWithServer(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline-validation-url").textContent);

        let response;
        try {
            response = await fetch(`${validationUrl}?` + new URLSearchParams({
                xml_file_string: metadataFile.xmlFileString,
                xml_file_name: metadataFile.name,
            }));
        } catch (error) {
            console.error("There was a problem whilst validating with the server.");
            const errorMsg = "A network error occurred.";
            return {
                metadataReferenceErrors: [errorMsg],
                ontologyReferenceErrors: [errorMsg],
            }
        }

        let results;
        try {
            results = await response.json();
        } catch (error) {
            if (response.status === 504) {
                const errorMsg = "Validation did not finish. The connection to the server timed out before validation could finish. Please try uploading the file again at a later time.";
                return {
                    metadataReferenceErrors: [errorMsg],
                    ontologyReferenceErrors: [errorMsg],
                };
            }
        }
        return {
            metadataReferenceErrors: results.incorrectly_structured_url_errors
                                        .concat(results.unregistered_operational_mode_url_errors)
                                        .concat(results.unregistered_resource_url_errors),
            ontologyReferenceErrors: results.invalid_ontology_url_errors,
            registrationErrors: results.xml_file_registration_errors,
        };
    }
}

class MetadataValidationStatusUIController {
    constructor(validationStatusListElem, fileInputElem) {
        this.validationStatusListElem = validationStatusListElem;
        this.fileInputElem = fileInputElem;
    }

    #htmlToElement(html) {
        const template = document.createElement("template");
        html = html.trim();
        template.innerHTML = html;
        return template.content.firstChild;
    }

    #removeMetadataFileAndRemoveFromValidationStatusList(metadataFile, i) {

    }

    #addSuccessValidationResults(successText, selector) {
        const statusElem = document.querySelector(selector);
        statusElem.innerHTML = `
        <div class="text-success">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
            </svg>${successText}
        </div>`;
    }

    #addFailedValidationResults(failureText, errors, selector) {
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

    #setAsValid(selector) {
        const mainStatusElem = document.querySelector(selector);
        mainStatusElem.className = "text-success";
        mainStatusElem.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
        </svg>Valid`;
    }

    #setAsInvalid(selector) {
        const mainStatusElem = document.querySelector(selector);
        mainStatusElem.className = "text-danger";
        mainStatusElem.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill text-danger me-2" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
        </svg>This metadata file is invalid.`;
    }

    #addMetadataFileToValidationStatusList(metadataFile) {
        this.validationStatusListElem.append(this.#htmlToElement(`
            <li class="list-group-item file-list-group-item-${metadataFile.id} p-4">
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
                        <summary class="text-secondary">
                            Validating
                        </summary>
                        <ul class="list-group list-group-flush mt-2" style="font-size: 0.8rem;">
                            <li class="list-group-item sv-list-group-item">
                                <details class="text-danger">
                                    <summary>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill text-danger me-2" viewBox="0 0 16 16">
                                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                                        </svg>Syntax
                                    </summary>
                                    <div class="pt-2">
                                        Errors:
                                        <ul>
                                            <li>error on line 1 at column 1: Document is empty</li>
                                        </ul>
                                    </div>
                                </details>
                            </li>
                            <li class="list-group-item renv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating type
                            </li>
                            <li class="list-group-item liv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating local ID
                            </li>
                            <li class="list-group-item nsv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating namespace
                            </li>
                            <li class="list-group-item mrv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating references to other metadata
                            </li>
                            <li class="list-group-item orv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating references to ontology references
                            </li>
                            <li class="list-group-item xv-list-group-item">
                                <div class="spinner-border spinner-border-sm me-2" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>Validating with XSD
                            </li>
                        </ul>
                    </details>
                </div>
            </li>
        `));
    }

    startValidation(metadataFile) {
        this.#addMetadataFileToValidationStatusList(metadataFile);
    }

    updateBasicValidationResults(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const svSelector = `.sv-list-group-item`;
        const nsvSelector = `.nsv-list-group-item`;
        const livSelector = `.liv-list-group-item`;
        const renvSelector = `.renv-list-group-item`;

        // Syntax validation results
        if (metadataFile.isSyntaxValid) {
            this.#addSuccessValidationResults(
                "Passed syntax validation.",
                `${fileListGroupItemSelector} ${svSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed syntax validation.",
                metadataFile.syntaxErrors,
                `${fileListGroupItemSelector} ${svSelector}`
            );
        }
        
        // Namespace validation results
        if (metadataFile.isNamespaceValid) {
            this.#addSuccessValidationResults(
                "Passed namespace validation.",
                `${fileListGroupItemSelector} ${nsvSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed namespace validation.",
                metadataFile.namespaceErrors,
                `${fileListGroupItemSelector} ${nsvSelector}`
            );
        }

        // Local ID validation results
        if (metadataFile.isLocalIDValid) {
            this.#addSuccessValidationResults(
                "Passed local ID validation.",
                `${fileListGroupItemSelector} ${livSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed local ID validation.",
                metadataFile.localIDErrors,
                `${fileListGroupItemSelector} ${livSelector}`
            );
        }

        // Root element name validation results
        if (metadataFile.isRootElementNameValid) {
            this.#addSuccessValidationResults(
                "Passed type validation.",
                `${fileListGroupItemSelector} ${renvSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed type validation.",
                metadataFile.rootElementNameErrors,
                `${fileListGroupItemSelector} ${renvSelector}`
            );
        }
    }

    updateReferenceValidationResults(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const mrvSelector = `.mrv-list-group-item`;
        const orvSelector = `.orv-list-group-item`;

        // Metadata reference validation results
        if (metadataFile.isEachMetadataReferenceValid) {
            this.#addSuccessValidationResults(
                "Passed metadata reference validation.",
                `${fileListGroupItemSelector} ${mrvSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed metadata reference validation.",
                metadataFile.metadataReferenceErrors,
                `${fileListGroupItemSelector} ${orvSelector}`
            );
        }
        
        // Ontology reference validation results
        if (metadataFile.isEachOntologyReferenceValid) {
            this.#addSuccessValidationResults(
                "Passed ontology reference validation.",
                `${fileListGroupItemSelector} ${orvSelector}`
            );
        } else {
            this.#addFailedValidationResults(
                "Failed ontology reference validation.",
                metadataFile.ontologyReferenceErrors,
                `${fileListGroupItemSelector} ${orvSelector}`
            );
        }
    }

    updateXsdValidationResults(metadataFile) {

    }

    endValidation(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const mainSummarySelector = ".details-validation > summary";
        if (metadataFile.isValid) {
            return this.#setAsValid(`${fileListGroupItemSelector} ${mainSummarySelector}`);
        }
        return this.#setAsInvalid(`${fileListGroupItemSelector} ${mainSummarySelector}`);
    }
}

window.addEventListener("load", async () => {
    const validator = new MetadataFileValidator();
    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const fileInputElem = document.querySelector("#id_files");
    const validationStatusUIController = new MetadataValidationStatusUIController(metadataFileListElem, fileInputElem);

    // Files
    const files = [
        testFile,
        testFile,
        testFile,
    ];
    for (const file of files) {
        const metadataFile = await MetadataFile.fromFile(file);
        validationStatusUIController.startValidation(metadataFile);

        const basicValidationResults = validator.validateBasicComponents(metadataFile);
        console.log('basicValidationResults', basicValidationResults);
        metadataFile.addBasicValidationResults(basicValidationResults);
        validationStatusUIController.updateBasicValidationResults(metadataFile);

        const serverValidationResults = await validator.validateWithServer(metadataFile);
        console.log('serverValidationResults', serverValidationResults);
        metadataFile.addReferenceValidationResults(serverValidationResults);
        validationStatusUIController.updateReferenceValidationResults(metadataFile);

        validationStatusUIController.endValidation(metadataFile);
    }
});