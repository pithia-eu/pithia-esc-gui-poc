import {
    DynamicEditorTableWithTextArea,
} from "/static/metadata_editor/components/table_with_dynamic_textareas.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";


class InputDescriptionsTable extends DynamicEditorTableWithTextArea {
    constructor() {
        super(
            "#table-input-descriptions",
            "#table-input-descriptions tbody",
            "#add-idrow-button",
            ".remove-idrow-button",
            "#input-description-row-content-template",
            "input[name='input_descriptions_json']",
            "input[name='input_descriptions_extra_json']"
        );
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);
 
        this.setupDynamicTextAreaForNewRow(newRow, "textarea[name='input_description']");
        const inputParameterNameInput = newRow.querySelector("input[name='input_name']");
        const inputParameterDescriptionTextarea = newRow.querySelector("textarea[name='input_description']");
        const fields = [
            inputParameterNameInput,
            inputParameterDescriptionTextarea,
        ];
        fields.forEach(field => {
            field.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(
                    [inputParameterDescriptionTextarea],
                    [inputParameterNameInput]
                );
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    exportTableData() {
        const inputDescriptionObjects = [];
        this.rows.forEach(row => {
            const inputParameterNameInput = row.querySelector("input[name='input_name']");
            const inputParameterDescriptionTextarea = row.querySelector("textarea[name='input_description']");
            inputDescriptionObjects.push({
                name: inputParameterNameInput.value,
                description: inputParameterDescriptionTextarea.value,
            });
        });
        return inputDescriptionObjects;
    }

    loadPreviousData() {
        super.loadPreviousData();
        const previousData = JSON.parse(this.jsonOutputElement.value);
        if (!previousData) {
            return;
        }
        previousData.forEach((inputDescriptionObject, i) => {
            if (i !== 0) {
                this.addRow();
            }
            const inputParameterName = inputDescriptionObject.name;
            const inputParameterDescription = inputDescriptionObject.description;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);

            // Input parameter name
            const inputParameterNameInput = correspondingRow.querySelector("input[name='input_name']");
            inputParameterNameInput.value = inputParameterName

            // Input parameter description
            const inputParameterDescriptionTextarea = correspondingRow.querySelector("textarea[name='input_description']");
            const inputParameterDescriptionTextareaFacade = correspondingRow.querySelector("textarea[name='input_description'] ~ div");
            inputParameterDescriptionTextarea.value = inputParameterDescription;
            inputParameterDescriptionTextareaFacade.innerHTML = inputParameterDescription;
            
            checkAndSetRequiredAttributesForFields(
                [inputParameterDescriptionTextarea],
                [inputParameterNameInput]
            );
        });
    }
}

export function setupInputDescriptionsTable() {
    const inputDescriptionsTable = new InputDescriptionsTable();
    inputDescriptionsTable.setup();
    return inputDescriptionsTable;
}