import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    DynamicEditorTable,
} from "/static/metadata_editor/components/table_utils.js";


class KeywordsTable extends DynamicEditorTable {
    constructor() {
        super(
            "#table-project-keywords",
            "#table-project-keywords tbody",
            "#add-kwrow-button",
            ".remove-kwrow-button",
            "#keywords-row-content-template",
            "input[name='keywords_json']",
            "input[name='keywords_extra_json']"
        );
    }

    exportTableData() {
        const keywordObjects = [];
        this.rows.forEach(row => {
            const keywordTypeInput = row.querySelector("input[name='keyword_type']");
            const keywordTypeCodeInput = row.querySelector("input[name='keyword_type_code']");
            const keywordMultipleChoiceSelect = row.querySelector("select[name='keyword']");
            const selectedKeywordOptions = Array.from(keywordMultipleChoiceSelect.selectedOptions);
            keywordObjects.push({
                keywords: selectedKeywordOptions.map(option => option.value),
                type: {
                    codeList: keywordTypeCodeInput.value,
                    codeListValue: keywordTypeInput.value,
                }
            });
        });
        return keywordObjects;
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);

        const inputs = Array.from(newRow.querySelectorAll("input[name='keyword_type'], input[name='keyword_type_code']"));
        const selects = Array.from(newRow.querySelectorAll("select"));
        const allFields = [
            ...inputs,
            ...selects,
        ];
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(allFields, allFields);
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
        selects.forEach(select => {
            select.addEventListener("change", () => {
                checkAndSetRequiredAttributesForFields(allFields, allFields);
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    addRow() {
        const newRow = super.addRow();

        window.dispatchEvent(new CustomEvent("newKeywordsSelectsAdded", {
            detail: Array.from(newRow.querySelectorAll("select[name='keyword']")).map(select => select.id),
        }));
    }

    loadPreviousData() {
        super.loadPreviousData();
        const previousData = JSON.parse(editorForm.querySelector("input[name='keywords_json']").value);
        if (!previousData) {
            return;
        }
        for (let i = 0; i < previousData.length - 1; i++) {
            this.addRow();
        }
        previousData.forEach((keywordObject, i) => {
            const keywordType = keywordObject.type.codeListValue;
            const keywordTypeCode = keywordObject.type.codeList;
            const keywords = keywordObject.keywords;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);
    
            // Keyword type
            const keywordTypeInput = correspondingRow.querySelector("input[name='keyword_type']");
            keywordTypeInput.value = keywordType;
    
            // Keyword type code
            const keywordTypeCodeInput = correspondingRow.querySelector("input[name='keyword_type_code']");
            keywordTypeCodeInput.value = keywordTypeCode.replace("#", "");
    
            // Keywords
            // Populate the keyword select with the
            // data saved to the JSON field
            const keywordMultipleChoiceSelect = correspondingRow.querySelector("select[name='keyword']");
            keywords.forEach((kw, kwi) => {
                keywordMultipleChoiceSelect.options[kwi] = new Option(kw, kw);
                keywordMultipleChoiceSelect.querySelector(`option[value="${kw}"]`).selected = true;
            });
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: keywordMultipleChoiceSelect.id,
            }));
            const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll("input[name='keyword_type'], input[name='keyword_type_code'], select"));
            checkAndSetRequiredAttributesForFields(
                conditionalRequiredFields,
                conditionalRequiredFields,
            );
        });
    }
}

export function setupKeywordsTable() {
    const newKeywordsTable = new KeywordsTable();
    newKeywordsTable.setup();
    return newKeywordsTable;
}