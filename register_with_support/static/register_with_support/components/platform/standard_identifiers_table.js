import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";
import {
    DynamicEditorTable,
} from "/static/register_with_support/components/table_utils.js"


class StandardIdentifiersTable extends DynamicEditorTable {
    constructor() {
        super(
            "#table-standard-identifiers",
            "#table-standard-identifiers tbody",
            "#add-sirow-button",
            ".remove-sirow-button",
            "#standard-identifier-row-content-template",
            "input[name='standard_identifiers_json']"
        );
    }

    exportTableData() {
        const standardIdentifierObjects = [];
        this.rows.forEach(row => {
            const standardIdentifierAuthorityInput = row.querySelector("input[name='standard_identifier_authority']");
            const standardIdentifierValueInput = row.querySelector("input[name='standard_identifier']");
            standardIdentifierObjects.push({
                authority: standardIdentifierAuthorityInput.value,
                value: standardIdentifierValueInput.value,
            });
        });
        return standardIdentifierObjects;
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);

        const inputs = Array.from(newRow.querySelectorAll("input[name='standard_identifier_authority'], input[name='standard_identifier']"));
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(inputs, inputs);
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    loadPreviousData() {
        const previousData = JSON.parse(editorForm.querySelector("input[name='standard_identifiers_json']").value);
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
            const standardIdentifierAuthorityInput = correspondingRow.querySelector("input[name='standard_identifier_authority']");
            standardIdentifierAuthorityInput.value = standardIdentifierAuthority;
    
            // Standard identifier
            const standardIdentifierInput = correspondingRow.querySelector("input[name='standard_identifier']");
            standardIdentifierInput.value = standardIdentifier;
    
            const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll("input[name='standard_identifier_authority'], input[name='standard_identifier']"));
            checkAndSetRequiredAttributesForFields(
                conditionalRequiredFields,
                conditionalRequiredFields,
            );
        });
    }
}

export function setupStandardIdentifiersTable() {
    const newStandardIdentifiersTable = new StandardIdentifiersTable();
    newStandardIdentifiersTable.setup();
    return newStandardIdentifiersTable;
}