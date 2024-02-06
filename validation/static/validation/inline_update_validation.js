import {
    MetadataFile,
    MetadataFileValidator,
    MetadataValidationStatusUIController,
    startValidationProcess,
} from "/static/validation/inline_metadata_file_validation.js";
const fileInput = document.querySelector("#id_files");

export class MetadataFileUpdate extends MetadataFile {
    constructor(xmlFileString, xmlFileName) {
        super(xmlFileString, xmlFileName);
        this.updateErrors = undefined;
    }

    static async fromFile(xmlFile) {
        const xmlFileString = await xmlFile.text();
        return new MetadataFileUpdate(xmlFileString, xmlFile.name);
    }

    get isUpdateValid() {
        if (this.updateErrors === undefined) {
            return false;
        }
        return this.updateErrors.length === 0;
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
            this.isUpdateValid,
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
            this.updateErrors ? this.updateErrors : [],
        ].flat().length;
    }

    addUpdateValidationResults(results) {
        this.updateErrors = results.updateErrors;
    }

    addServerValidationResults(results) {
        this.addReferenceValidationResults(results);
        this.addUpdateValidationResults(results);
    }
}

export class MetadataFileUpdateValidator extends MetadataFileValidator {
    async serverValidationFetchRequest(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline-validation-url").textContent);
        const existingMetadataId = JSON.parse(document.getElementById("resource-id").textContent);
        
        return fetch(`${validationUrl}?` + new URLSearchParams({
            xml_file_string: metadataFile.xmlFileString,
            xml_file_name: metadataFile.name,
            existing_metadata_id: existingMetadataId,
        }));
    }

    serverValidationErrorObject(errorMsg) {
        return {
            metadataReferenceErrors: [errorMsg],
            ontologyReferenceErrors: [errorMsg],
            updateErrors: [errorMsg],
        };
    }

    serverValidationResultsObject(results) {
        return {
            metadataReferenceErrors: results.incorrectly_structured_url_errors
                                        .concat(results.unregistered_operational_mode_url_errors)
                                        .concat(results.unregistered_resource_url_errors),
            ontologyReferenceErrors: results.invalid_ontology_url_errors,
            updateErrors: results.xml_file_update_errors,
        };
    }
}

export class MetadataUpdateValidationStatusUIController extends MetadataValidationStatusUIController {
    addUpdateValidationStatusListItemForMetadataFile(metadataFile) {
        const statusList = document.querySelector(`.file-list-group-item-${metadataFile.id} .details-validation ul`);
        statusList.append(this.htmlToElement(`
            <li class="uv-list-group-item py-2">
                <div class="text-secondary">
                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>Validating update
                </div>
            </li>
        `));
    }

    addMetadataFileToValidationStatusList(metadataFile) {
        this.addGenericListItemForMetadataFile(metadataFile);
        this.addUpdateValidationStatusListItemForMetadataFile(metadataFile);
    }

    updateUpdateValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const uvSelector = `.uv-list-group-item`;

        // Update validation results
        if (metadataFile.isUpdateValid) {
            this.addSuccessValidationResultsForFile(
                "This file can be used as an update.",
                `${fileListGroupItemSelector} ${uvSelector}`
            );
        } else {
            this.addFailedValidationResultsForFile(
                "Failed update validation.",
                metadataFile.updateErrors,
                `${fileListGroupItemSelector} ${uvSelector}`
            );
        }
    }

    updateServerValidationResultsForFile(metadataFile) {
        this.updateReferenceValidationResultsForFile(metadataFile);
        this.updateUpdateValidationResultsForFile(metadataFile);
    }
}

export async function startMetadataFileUpdateValidationProcess() {
    const files = Array.from(fileInput.files);
    const validator = new MetadataFileUpdateValidator();

    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const validationStatusUIController = new MetadataUpdateValidationStatusUIController(metadataFileListElem, fileInput);
    const newMetadataFileObjectFn = MetadataFileUpdate.fromFile;

    return startValidationProcess(files, validator, validationStatusUIController, newMetadataFileObjectFn);
}