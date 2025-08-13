import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    DynamicEditorTable,
} from "/static/metadata_editor/components/table_utils.js"


export class StandardIdentifiersTable extends DynamicEditorTable {
    constructor(
        tableSelector,
        tableBodySelector,
        addRowButtonSelector,
        removeRowButtonSelector,
        rowContentTemplateSelector,
        jsonOutputSelector,
        standardIdentifierAuthorityInputSelector,
        standardIdentifierInputSelector
    ) {
        super(
            tableSelector,
            tableBodySelector,
            addRowButtonSelector,
            removeRowButtonSelector,
            rowContentTemplateSelector,
            jsonOutputSelector
        );
        this.standardIdentifierAuthorityInputSelector = standardIdentifierAuthorityInputSelector;
        this.standardIdentifierInputSelector = standardIdentifierInputSelector;
        this.standardIdentifiersJsonInputSelector = jsonOutputSelector;
    }

    exportTableData() {
        const standardIdentifierObjects = [];
        this.rows.forEach(row => {
            const standardIdentifierAuthorityInput = row.querySelector(this.standardIdentifierAuthorityInputSelector);
            const standardIdentifierValueInput = row.querySelector(this.standardIdentifierInputSelector);
            standardIdentifierObjects.push({
                authority: standardIdentifierAuthorityInput.value,
                value: standardIdentifierValueInput.value,
            });
        });
        return standardIdentifierObjects;
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);

        const inputs = Array.from(
            newRow.querySelectorAll(`${this.standardIdentifierAuthorityInputSelector}, ${this.standardIdentifierInputSelector}`)
        );
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(inputs, inputs);
                window.dispatchEvent(new CustomEvent("validateFields", {
                    detail: {
                        fieldIds: inputs.map(input => input.id),
                    }
                }));
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    loadPreviousData() {
        super.loadPreviousData();
        const previousDataJsonString = editorForm.querySelector(this.standardIdentifiersJsonInputSelector).value;
        if (!previousDataJsonString.trim()) {
            return;
        }
        let previousData;
        try {
            previousData = JSON.parse(previousDataJsonString);
        } catch (error) {
            console.error('Could not load previous standard identifiers data.');
            return;
        }
        if (!previousData) {
            return;
        }
        for (let i = 0; i < previousData.length - 1; i++) {
            this.addRow();
        }
        previousData.forEach((standardIdentifierObject, i) => {
            const standardIdentifierAuthority = standardIdentifierObject.authority;
            const standardIdentifier = standardIdentifierObject.value;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);
    
            // Standard identifier authority
            const standardIdentifierAuthorityInput = correspondingRow.querySelector(this.standardIdentifierAuthorityInputSelector);
            standardIdentifierAuthorityInput.value = standardIdentifierAuthority;
    
            // Standard identifier
            const standardIdentifierInput = correspondingRow.querySelector(this.standardIdentifierInputSelector);
            standardIdentifierInput.value = standardIdentifier;
    
            const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll(`${this.standardIdentifierAuthorityInputSelector}, ${this.standardIdentifierInputSelector}`));
            checkAndSetRequiredAttributesForFields(
                conditionalRequiredFields,
                conditionalRequiredFields,
            );
        });
    }
}