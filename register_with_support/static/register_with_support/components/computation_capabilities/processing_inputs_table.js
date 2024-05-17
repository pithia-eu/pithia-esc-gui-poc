import {
    DynamicEditorTableWithTextArea,
} from "/static/register_with_support/components/table_with_dynamic_textareas.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";


class ProcessingInputsTable extends DynamicEditorTableWithTextArea {
    constructor() {
        super(
            "#table-processing-inputs",
            "#table-processing-inputs tbody",
            "#add-pirow-button",
            ".remove-pirow-button",
            "#processing-input-row-content-template",
            "input[name='processing_inputs_json']"
        );
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);
 
        this.setupDynamicTextAreaForNewRow(newRow, "textarea[name='processing_input_description']");
        const processingInputNameInput = newRow.querySelector("input[name='processing_input_name']");
        const processingInputDescriptionTextarea = newRow.querySelector("textarea[name='processing_input_description']");
        const fields = [
            processingInputNameInput,
            processingInputDescriptionTextarea,
        ];
        fields.forEach(field => {
            field.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(
                    [processingInputDescriptionTextarea],
                    [processingInputNameInput]
                );
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    exportTableData() {
        const processingInputObjects = [];
        this.rows.forEach(row => {
            const processingInputNameInput = row.querySelector("input[name='processing_input_name']");
            const processingInputDescriptionTextarea = row.querySelector("textarea[name='processing_input_description']");
            processingInputObjects.push({
                name: processingInputNameInput.value,
                description: processingInputDescriptionTextarea.value,
            });
        });
        return processingInputObjects;
    }

    loadPreviousData() {
        const previousData = JSON.parse(this.jsonOutputElement.value);
        if (!previousData) {
            return;
        }
        previousData.forEach((processingInputObject, i) => {
            if (i !== 0) {
                this.addRow();
            }
            const processingInputName = processingInputObject.name;
            const processingInputDescription = processingInputObject.description;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);

            // Processing input name
            const processingInputNameInput = correspondingRow.querySelector("input[name='processing_input_name']");
            processingInputNameInput.value = processingInputName

            // Processing input description
            const processingInputDescriptionTextarea = correspondingRow.querySelector("textarea[name='processing_input_description']");
            const processingInputDescriptionTextareaFacade = correspondingRow.querySelector("textarea[name='processing_input_description'] ~ div");
            processingInputDescriptionTextarea.value = processingInputDescription;
            processingInputDescriptionTextareaFacade.innerHTML = processingInputDescription;
            
            checkAndSetRequiredAttributesForFields(
                [processingInputDescriptionTextarea],
                [processingInputNameInput]
            );
        });
    }
}

export function setupProcessingInputsTable() {
    const processingInputsTable = new ProcessingInputsTable();
    processingInputsTable.setup();
    return processingInputsTable;
}