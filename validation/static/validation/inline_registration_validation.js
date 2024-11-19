import {
    MetadataFile,
    MetadataFileValidator,
    MetadataValidationStatusUIController,
    startValidationProcess,
} from "/static/validation/inline_metadata_file_validation.js";
const fileInput = document.querySelector("#id_files");

export class NewMetadataFile extends MetadataFile {
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

    get isValid() {
        const isEachBaseCheckValid = super.isValid;
        return [
            isEachBaseCheckValid,
            this.isNotRegisteredAlready,
        ].every(result => result === true);
    }

    get totalErrorCount() {
        const baseTotalErrorCount = super.totalErrorCount;
        return baseTotalErrorCount + (this.newRegistrationErrors ? this.newRegistrationErrors : []).length;
    }

    #addNewRegistrationValidationResults(results) {
        this.newRegistrationErrors = results.newRegistrationErrors;
    }

    addServerValidationResults(results) {
        this.addReferenceValidationResults(results);
        this.#addNewRegistrationValidationResults(results);
    }
}

export class NewMetadataFileValidator extends MetadataFileValidator {
    async serverValidationFetchRequest(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline-validation-url").textContent);

        const formData = new FormData();
        const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        formData.append("csrfmiddlewaretoken", csrfMiddlewareToken);
        formData.append("xml_file_string", metadataFile.xmlFileString);
        formData.append("xml_file_name", metadataFile.name);

        return fetch(validationUrl, {
            method: "POST",
            body: formData,
        });
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

export class NewMetadataValidationStatusUIController extends MetadataValidationStatusUIController {
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
        if (metadataFile.isNotRegisteredAlready) {
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

export async function startNewRegistrationValidationProcess() {
    const files = Array.from(fileInput.files);
    const validator = new NewMetadataFileValidator();

    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const validationStatusUIController = new NewMetadataValidationStatusUIController(metadataFileListElem, fileInput);
    const newMetadataFileObjectFn = NewMetadataFile.fromFile;

    return startValidationProcess(files, validator, validationStatusUIController, newMetadataFileObjectFn);
}