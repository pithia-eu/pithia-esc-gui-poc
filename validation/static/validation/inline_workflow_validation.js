import {
    startValidationProcess,
} from "/static/validation/inline_metadata_file_validation.js";
import {
    NewMetadataFile,
    NewMetadataFileValidator,
    NewMetadataValidationStatusUIController,
} from "/static/validation/inline_registration_validation.js";
import {
    MetadataFileUpdate,
    MetadataFileUpdateValidator,
    MetadataUpdateValidationStatusUIController,
} from "/static/validation/inline_update_validation.js";


const fileInput = document.querySelector("#id_files");
const WorkflowMetadataFile = Base => class extends Base {
    constructor(xmlFileString, xmlFileName) {
        super(xmlFileString, xmlFileName);
        this.workflowDetailsUrlWarnings = undefined;
    }

    get isWorkflowDetailsUrlValidationComplete() {
        if (this.workflowDetailsUrlWarnings === undefined) {
            return false;
        }
        return this.workflowDetailsUrlWarnings.length === 0;
    }

    getTotalWarningCount() {
        return (this.workflowDetailsUrlWarnings ? this.workflowDetailsUrlWarnings : []).length;
    }

    addBasicValidationResults(results) {
        super.addBasicValidationResults(results);
        this.workflowDetailsUrlWarnings = results.workflowDetailsUrlWarnings;
    }
}
const WorkflowMetadataFileValidator = Base => class extends Base {
    validateWorkflowDetailsUrl(xmlDoc) {
        const workflowDetails = xmlDoc.querySelector("workflowDetails");
        const errors = [];

        // Check if workflowDetails element is present.
        if (workflowDetails === null) {
            errors.push("A workflowDetails element was not found in your metadata file.")
            return errors;
        }

        const workflowDetailsUrlValue = workflowDetails.getAttribute('xlink:href');
        // Check the workflowDetails URL is valid and is not internal.
        try {
            const workflowDetailsUrl = new URL(workflowDetailsUrlValue);
            if (workflowDetailsUrl.hostname == "esc.pithia.eu") {
                errors.push("Please use the provided workflow details file input to register the details file with this workflow.");
            }
        } catch (error) {
            console.error(error);
            errors.push("The workflow details URL is not valid.");
        }

        return errors;
    }

    validateBasicComponents(metadataFile) {
        const validationResults = super.validateBasicComponents(metadataFile)
        const xmlDoc = metadataFile.xmlDoc;
        
        const workflowDetailsUrlWarnings = validationResults.syntaxErrors.length > 0 ? [COULD_NOT_CHECK_ERROR] : this.validateWorkflowDetailsUrl(xmlDoc);
        validationResults.workflowDetailsUrlWarnings = workflowDetailsUrlWarnings;

        return validationResults;
    }
}
const WorkflowMetadataValidationStatusUIController = Base => class extends Base {
    #addWorkflowValidationStatusListItemForMetadataFile(metadataFile) {
        const statusList = document.querySelector(`.file-list-group-item-${metadataFile.id} .details-validation ul`);
        statusList.append(this.htmlToElement(`
            <li class="wv-list-group-item py-2">
                <div class="text-secondary">
                    <div class="spinner-grow spinner-grow-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>Validating link to workflow details file
                </div>
            </li>
        `));
    }

    #addWarningValidationResultsForFile(warningText, warnings, selector) {
        const statusElem = document.querySelector(selector);
        let warningLisString = "";
        warnings.forEach(e => warningLisString += `<li>${e}</li>`);
        statusElem.innerHTML = `
        <details>
            <summary>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-triangle-fill text-warning me-2" viewBox="0 0 16 16">
                    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"/>
                </svg>${warningText}
            </summary>
            <div class="pt-2">
                <ul>
                    ${warningLisString}
                </ul>
            </div>
        </details>`;
    }

    addMetadataFileToValidationStatusList(metadataFile) {
        super.addMetadataFileToValidationStatusList(metadataFile);
        this.#addWorkflowValidationStatusListItemForMetadataFile(metadataFile);
    }

    #updateTotalWarningCountForFile(metadataFile) {
        const warningNumElem = document.querySelector(`.file-list-group-item-${metadataFile.id} .num-warnings`);
        warningNumElem.innerHTML = metadataFile.workflowDetailsUrlWarnings.length > 1 ? metadataFile.workflowDetailsUrlWarnings.length + " warnings" : metadataFile.workflowDetailsUrlWarnings.length + " warning";
    }

    #updateWorkflowValidationResultsForFile(metadataFile) {
        const fileListGroupItemSelector = `.file-list-group-item-${metadataFile.id}`;
        const wvSelector = `.wv-list-group-item`;

        // Workflow details URL validation results
        if (!metadataFile.isWorkflowDetailsUrlValidationComplete) {
            this.#addWarningValidationResultsForFile(
                "Some problems were found with the workflow details file link. These are only applicable if you are not uploading/have not uploaded your workflow details file to the e-Science Centre.",
                metadataFile.workflowDetailsUrlWarnings,
                `${fileListGroupItemSelector} ${wvSelector}`
            );

            this.#updateTotalWarningCountForFile(metadataFile);
            return;
        }

        return this.addSuccessValidationResultsForFile(
            "Passed workflow details URL validation.",
            `${fileListGroupItemSelector} ${wvSelector}`
        );
    }

    updateBasicValidationResultsForFile(metadataFile) {
        super.updateBasicValidationResultsForFile(metadataFile);
        this.#updateWorkflowValidationResultsForFile(metadataFile);
    }
}

class NewWorkflowMetadataFile extends WorkflowMetadataFile(NewMetadataFile) {}
class NewWorkflowMetadataFileValidator extends WorkflowMetadataFileValidator(NewMetadataFileValidator) {}
class NewWorkflowMetadataValidationStatusUIController extends WorkflowMetadataValidationStatusUIController(NewMetadataValidationStatusUIController) {}

export async function startNewWorkflowMetadataFileValidationProcess() {
    const files = Array.from(fileInput.files);
    const validator = new NewWorkflowMetadataFileValidator();

    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const validationStatusUIController = new NewWorkflowMetadataValidationStatusUIController(metadataFileListElem, fileInput);
    const newMetadataFileObjectFn = async xmlFile => {
        const xmlFileString = await xmlFile.text();
        return new NewWorkflowMetadataFile(xmlFileString, xmlFile.name);
    };

    return startValidationProcess(files, validator, validationStatusUIController, newMetadataFileObjectFn);
}

class WorkflowUpdateMetadataFile extends WorkflowMetadataFile(MetadataFileUpdate) {}
class WorkflowUpdateMetadataFileValidator extends WorkflowMetadataFileValidator(MetadataFileUpdateValidator) {}
class WorkflowUpdateMetadataValidationStatusUIController extends WorkflowMetadataValidationStatusUIController(MetadataUpdateValidationStatusUIController) {}

export async function startWorkflowMetadataFileUpdateValidationProcess() {
    const files = Array.from(fileInput.files);
    const validator = new WorkflowUpdateMetadataFileValidator();

    const metadataFileListElem = document.querySelector(".file-validation-status-list");
    const validationStatusUIController = new WorkflowUpdateMetadataValidationStatusUIController(metadataFileListElem, fileInput);
    const newMetadataFileObjectFn = async xmlFile => {
        const xmlFileString = await xmlFile.text();
        return new WorkflowUpdateMetadataFile(xmlFileString, xmlFile.name);
    };

    return startValidationProcess(files, validator, validationStatusUIController, newMetadataFileObjectFn);
}

