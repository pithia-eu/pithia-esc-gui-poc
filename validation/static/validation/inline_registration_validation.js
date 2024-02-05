import {
    MetadataFile,
    MetadataFileValidator,
    MetadataValidationStatusUIController,
    testFile1,
    testFile2,
    testFile3,
    validateMetadataFile,
} from "/static/validation/inline_metadata_file_validation.js";
const fileInput = document.querySelector("#id_files");

class NewMetadataFile extends MetadataFile {
    constructor(xmlFileString, xmlFileName) {
        super(xmlFileString, xmlFileName);
        this.newRegistrationErrors = undefined;
    }

    static async fromFile(xmlFile) {
        const xmlFileString = await xmlFile.text();
        return new NewMetadataFile(xmlFileString, xmlFile.name);
    }

    get isNotRegisteredAlready() {
        if (this.newRegistrationErrors === undefined) {
            return false;
        }
        return this.newRegistrationErrors.length === 0;
    }

    #addNewRegistrationValidationResults(results) {
        this.newRegistrationErrors = results.newRegistrationErrors;
    }

    addServerValidationResults(results) {
        this.addReferenceValidationResults(results);
        this.#addNewRegistrationValidationResults(results);
    }
}

class NewMetadataFileValidator extends MetadataFileValidator {
    async serverValidationFetchRequest(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline-validation-url").textContent);

        return fetch(`${validationUrl}?` + new URLSearchParams({
            xml_file_string: metadataFile.xmlFileString,
            xml_file_name: metadataFile.name,
        }));
    }

    serverValidationErrorObject(errorMsg) {
        return {
            metadataReferenceErrors: [errorMsg],
            ontologyReferenceErrors: [errorMsg],
            newRegistrationErrors: [errorMsg],
        };
    }

    serverValidationResultsObject(results) {
        return {
            metadataReferenceErrors: results.incorrectly_structured_url_errors
                                        .concat(results.unregistered_operational_mode_url_errors)
                                        .concat(results.unregistered_resource_url_errors),
            ontologyReferenceErrors: results.invalid_ontology_url_errors,
            newRegistrationErrors: results.xml_file_registration_errors,
        };
    }
}

class NewMetadataValidationStatusUIController extends MetadataValidationStatusUIController {
    #addRegistrationValidationStatusListItemForMetadataFile(metadataFile) {
        const statusList = document.querySelector(`.file-list-group-item-${metadataFile.id} .details-validation ul`);
        statusList.append(this.htmlToElement(`
            <li class="rv-list-group-item py-2">
                <div class="text-secondary">
                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>Validating new registration
                </div>
            </li>
        `));
    }

    addMetadataFileToValidationStatusList(metadataFile) {
        this.addGenericListItemForMetadataFile(metadataFile);
        this.#addRegistrationValidationStatusListItemForMetadataFile(metadataFile);
    }

    #updateNewRegistrationValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const rvSelector = `.rv-list-group-item`;

        // New registration validation results
        if (metadataFile.isEachMetadataReferenceValid) {
            this.addSuccessValidationResultsForFile(
                "This file has not yet been registered.",
                `${fileListGroupItemSelector} ${rvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed new registration validation.",
                metadataFile.newRegistrationErrors,
                `${fileListGroupItemSelector} ${rvSelector}`
            );
        }
    }

    updateServerValidationResultsForFile(metadataFile) {
        this.updateReferenceValidationResultsForFile(metadataFile);
        this.#updateNewRegistrationValidationResultsForFile(metadataFile);
    }
}

async function startValidationProcess() {
    // const files = Array.from(fileInput.files);
    const files = [
        testFile1,
        testFile2,
        testFile3,
    ];
    const validator = new NewMetadataFileValidator();

    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const validationStatusUIController = new NewMetadataValidationStatusUIController(metadataFileListElem, fileInput);

    const validationRequests = [];
    for (const file of files) {
        const metadataFile = await NewMetadataFile.fromFile(file);
        validationRequests.push(validateMetadataFile(metadataFile, validator, validationStatusUIController));
    };
    await Promise.all(validationRequests);
}

fileInput.addEventListener("change", async event => {
    await startValidationProcess();
});

window.addEventListener("load", async event => {
    // if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startValidationProcess();
    // }
});