import {
    DynamicEditorTable,
} from "/static/register_with_support/components/table_utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";


class OperationalModesTable extends DynamicEditorTable {
    constructor() {
        super(
            "#table-operational-modes",
            "#table-operational-modes tbody",
            "#add-omrow-button",
            ".remove-omrow-button",
            "#operational-mode-row-content-template",
            "input[name='operational_modes_json']"
        );
    }

    exportTableData() {
        const operationalModeObjects = [];
        this.rows.forEach(row => {
            const operationalModeIdInput = row.querySelector("input[name='operational_mode_id']");
            const operationalModeNameInput = row.querySelector("input[name='operational_mode_name']");
            const operationalModeDescriptionTextarea = row.querySelector("textarea[name='operational_mode_description']");
            operationalModeObjects.push({
                id: operationalModeIdInput.value,
                name: operationalModeNameInput.value,
                description: operationalModeDescriptionTextarea.value,
            });
        });
        return operationalModeObjects;
    }

    setupOperationalModeDescriptionTextareaForNewRow(newRow) {
        const operationalModeDescriptionTextarea = newRow.querySelector("textarea[name='operational_mode_description']");
        const operationalModeDescriptionDiv = newRow.querySelector("textarea[name='operational_mode_description'] ~ div");
    
        operationalModeDescriptionTextarea.addEventListener("focus", () => {
            operationalModeDescriptionTextarea.style.height = operationalModeDescriptionTextarea.scrollHeight + "px";
        });
        
        operationalModeDescriptionTextarea.addEventListener("input", () => {
            operationalModeDescriptionTextarea.style.height = operationalModeDescriptionTextarea.scrollHeight + "px";
            operationalModeDescriptionDiv.innerHTML = operationalModeDescriptionTextarea.value;
            this.exportTableDataToJsonAndStoreInOutputElement();
        });
        
        operationalModeDescriptionTextarea.addEventListener("blur", () => {
            operationalModeDescriptionTextarea.removeAttribute("style");
        });
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);
 
        this.setupOperationalModeDescriptionTextareaForNewRow(newRow);
        const fields = Array.from(newRow.querySelectorAll("input[name='operational_mode_id'], input[name='operational_mode_name'], textarea[name='operational_mode_description']"));
        fields.forEach(field => {
            field.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(fields, fields);
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    loadPreviousData() {
        const previousData = JSON.parse(document.querySelector("input[name='operational_modes_json']").value);
        if (!previousData) {
            return;
        }
        for (let i = 0; i < previousData.length - 1; i++) {
            this.addRow();
        }
        previousData.forEach((operationalModeObject, i) => {
            const operationalModeId = operationalModeObject.id;
            const operationalModeName = operationalModeObject.name;
            const operationalModeDescription = operationalModeObject.description;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);
    
            // Operational mode ID
            const operationalModeIdInput = correspondingRow.querySelector("input[name='operational_mode_id']");
            operationalModeIdInput.value = operationalModeId;
    
            // Operational mode name
            const operationalModeNameInput = correspondingRow.querySelector("input[name='operational_mode_name']");
            operationalModeNameInput.value = operationalModeName;
    
            // Operational mode description
            const operationalModeDescriptionTextarea = correspondingRow.querySelector("textarea[name='operational_mode_description']");
            const operationalModeDescriptionDiv = correspondingRow.querySelector("textarea[name='operational_mode_description'] ~ div");
            operationalModeDescriptionTextarea.value = operationalModeDescription;
            operationalModeDescriptionDiv.innerHTML = operationalModeDescription;
    
            const conditionalRequiredFields = [
                operationalModeIdInput,
                operationalModeNameInput,
                operationalModeDescriptionTextarea,
            ];
            checkAndSetRequiredAttributesForFields(
                conditionalRequiredFields,
                conditionalRequiredFields
            );
        });
    }
}

export function setupOperationalModesTable() {
    const newOperationalModesTable = new OperationalModesTable();
    newOperationalModesTable.setup();
    return newOperationalModesTable;
}