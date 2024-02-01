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
        this.isSyntaxValid = false;
        this.isNamespaceValid = false;
        this.isLocalIDValid = false;
        this.isRootElementNameValid = false;
        this.isEachElementAllowed = false;
        this.isEachMetadataReferenceValid = false;
        this.isEachOntologyReferenceValid = false;
    }

    static async fromFile(xmlFile) {
        const xmlFileString = await testFile.text();
        return new MetadataFile(xmlFileString, xmlFile.name);
    }

    get isValid() {
        return [
            this.isSyntaxValid,
            this.isNamespaceValid,
            this.isLocalIDValid,
            this.isRootElementNameValid,
            this.isEachElementAllowed,
            this.isEachMetadataReferenceValid,
            this.isEachOntologyReferenceValid,
        ].every(e => e === e);
    }

    addQuickSectionValidationResults(results) {

    }

    addServerValidationResults(results) {

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
        console.log("localID.textContent", localID.textContent);

        // Check if the localID is matching with the file name.
        if (localID.textContent !== this.removeFileExtensionFromString(xmlFileName)) {
            errors.push(`The localID (${localID.textContent}) must be matching the the name of the file (${xmlFileName}).`);
        }

        // Check localID content.
        const re = new RegExp("^[\w-]+$");
        if (re.exec(localID.textContent) !== null) {
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
        const re = new RegExp("^[\w-]+$");
        console.log("re.exec(namespace.textContent)", re.exec(namespace.textContent));
        if (re.exec(namespace.textContent) !== null) {
            errors.push("The namespace can only contain alphanumeric characters with optional use of dashes and/or underscores.");
        }

        return errors;
    }

    validateQuickSections(metadataFile) {
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
        const validationUrl = JSON.parse(document.getElementById("inline_validation_url").textContent);
        const response = await fetch(`${validationUrl}?` + new URLSearchParams({
            xml_file_string: metadataFile.xmlFileString,
            xml_file_name: metadataFile.name,
        }));
        const results = await response.json();
        return results;
    }
}

class MetadataValidationUIController {
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

    #addMetadataFileToValidationStatusList(metadataFile) {
        this.validationStatusListElem.append(this.#htmlToElement(`
            <li class="list-group-item file-list-group-item-${metadataFile.id} p-4">
                <div class="d-flex flex-column flex-grow-1">
                    <div class="pb-3">
                        <div class="d-flex align-items-center w-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-xml flex-shrink-0 me-3" viewBox="0 0 16 16" style="width: 1.2rem; height: 1.2rem;">
                                <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2v-1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM3.527 11.85h-.893l-.823 1.439h-.036L.943 11.85H.012l1.227 1.983L0 15.85h.861l.853-1.415h.035l.85 1.415h.908l-1.254-1.992 1.274-2.007Zm.954 3.999v-2.66h.038l.952 2.159h.516l.946-2.16h.038v2.661h.715V11.85h-.8l-1.14 2.596h-.025L4.58 11.85h-.806v3.999h.706Zm4.71-.674h1.696v.674H8.4V11.85h.791v3.325Z"/>
                            </svg>
                            <span class="text-truncate me-auto">${file.name}</span>
                            <button id="btn-rm-file-${metadataFile.id}" class="btn btn-outline-dark btn-sm btn-rm-file" data-list-item-num="${metadataFile.id}" type="button">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill pe-none" viewBox="0 0 16 16">
                                    <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="d-flex flex-column file-upload-validation-msgs">
                        <input type="hidden" id="is-file-${metadataFile.id}-valid" class="is-file-valid-status" value="false">
                        <div class="col-lg-12 file-validation-status file-validation-status-${metadataFile.id} text-break">
                        </div>
                        <div class="col-lg-12 file-validation-warnings file-validation-warnings-${metadataFile.id} text-break d-none">
                            <ul class="list-group list-group-warning">
                            </ul>
                        </div>
                        <div class="col-lg-12 file-validation-error file-validation-error-${metadataFile.id} text-break d-none">
                        </div>
                    </div>
                </div>
            </li>
        `));
    }

    startValidation(metadataFile) {
        this.#addMetadataFileToValidationStatusList(metadataFile);
    }

    updateQuickValidationResults(metadataFile) {

    }

    updateServerValidationResults(metadataFile) {

    }

    updateXsdValidationResults(metadataFile) {

    }

    endValidation(metadataFile) {

    }
}

window.addEventListener("load", async () => {
    const validator = new MetadataFileValidator();

    console.log("Valid XML");
    const validMetadataFile = new MetadataFile(testXml, "Organisation_Test.xml");
    const validXmlResults = validator.validateQuickSections(validMetadataFile);
    const validXmlServerResults = await validator.validateRegistrationWithDatabaseAndOntology(validMetadataFile);
    console.log('validXmlResults', validXmlResults);
    console.log('validXmlServerResultsvalidXmlResults', validXmlServerResults);
    
    console.log("Invalid XML");
    const invalidMetadataFile = new MetadataFile(invalidTestXml, "Organisation_Test.xml");
    const invalidXmlResults = validator.validateQuickSections(invalidMetadataFile);
    console.log('invalidXmlResults', invalidXmlResults);

    console.log("Xml file test");
    const testMetadataFileWithAltConstructor = await MetadataFile.fromFile(testFile);
    const testMetadataFileWithAltConstructorResults = validator.validateQuickSections(testMetadataFileWithAltConstructor);
    console.log('testMetadataFileWithAltConstructorResults', testMetadataFileWithAltConstructorResults);
});