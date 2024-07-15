import {
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/metadata_editor/components/utils.js";


export class DynamicEditorTable {
    constructor(tableSelector, tableBodySelector, addRowButtonSelector, removeRowButtonSelector, rowContentTemplateSelector, jsonOutputSelector, jsonExtraOutputSelector) {
        this.table = document.querySelector(tableSelector);
        this.tableBody = document.querySelector(tableBodySelector);
        this.rowContentTemplate = JSON.parse(document.querySelector(rowContentTemplateSelector).textContent);
        this.addRowButton = document.querySelector(addRowButtonSelector);
        this.removeRowButtonSelector = removeRowButtonSelector;
        this.jsonOutputElement = document.querySelector(jsonOutputSelector);
        this.jsonExtraOutputElement = document.querySelector(jsonExtraOutputSelector);
        this.rowAdditionsAndDeletions = [];
    }

    // Getters
    get rows() {
        return this.tableBody.querySelectorAll("tr");
    }

    // Initial setup
    setup() {
        const firstRow = this.tableBody.querySelector("tr");
        this.setupNewRowEventListeners(firstRow);
        this.loadPreviousData();
        this.setupAddRowButton();
    }

    // Utils
    getParentRowOfChildNode(childNode) {
        for (const row of this.rows) {
            if (row.contains(childNode)) {
                return row;
            }
        }
        return null;
    }

    disableFirstRemoveRowButtonIfOnlyOneRow() {
        const firstRemoveRowButton = this.tableBody.querySelector(this.removeRowButtonSelector);
        firstRemoveRowButton.disabled = this.rows.length === 1;
    }

    getRowNumber(row) {
        return Array.from(this.tableBody.children).indexOf(row);
    }

    // JSON export
    exportTableData() {
        // Implemented in child class
    }

    updateAndExportTableRowAddAndDeleteData(addOrDeleteAction, deletedRowNumber = -1) {
        if (addOrDeleteAction === "delete") {
            addOrDeleteAction = `${addOrDeleteAction}${deletedRowNumber}`;
        }
        this.rowAdditionsAndDeletions.push(addOrDeleteAction);
        const jsonExtraOutputData = JSON.parse(this.jsonExtraOutputElement.value);
        jsonExtraOutputData.rowAdditionsAndDeletions = this.rowAdditionsAndDeletions;
        this.jsonExtraOutputElement.value = JSON.stringify(jsonExtraOutputData);
        window.dispatchEvent(new CustomEvent("dynamicTableDataExported"));
    }

    exportTableDataToJsonAndStoreInOutputElement() {
        const tableExportData = JSON.stringify(this.exportTableData());
        this.jsonOutputElement.value = tableExportData;
        window.dispatchEvent(new CustomEvent("dynamicTableDataExported"));
    }

    // New row setup
    setupDuplicatedContentInNewRow(newRow) {
        const removeRowButton = newRow.querySelector(this.removeRowButtonSelector);
        removeRowButton.disabled = false;

        // Ensure the any element IDs in the
        // row content template are unique.
        const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
        updateDuplicatedElemsWithIdsInContainer(childElementsWithIdAttribute, newRow);
    }

    setupNewRowEventListeners(newRow) {
        const newRemoveRowButton = newRow.querySelector(this.removeRowButtonSelector);
        this.setupNewRemoveRowButton(newRemoveRowButton);
    }
    
    addRow() {
        const newRow = document.createElement("TR");
        newRow.innerHTML = this.rowContentTemplate;

        this.setupDuplicatedContentInNewRow(newRow);
        this.setupNewRowEventListeners(newRow);

        this.tableBody.appendChild(newRow);
        this.disableFirstRemoveRowButtonIfOnlyOneRow();

        return newRow;
    }

    addRowButtonOnClick = () => {
        this.addRow();
        this.exportTableDataToJsonAndStoreInOutputElement();
        this.updateAndExportTableRowAddAndDeleteData("add");
    }

    setupAddRowButton() {
        this.addRowButton.addEventListener("click", this.addRowButtonOnClick);
    }

    // Row removal
    removeRow(rowChildNode) {
        const containingRow = this.getParentRowOfChildNode(rowChildNode);
        const containingRowNumber = this.getRowNumber(containingRow);
        this.tableBody.removeChild(containingRow);
        this.disableFirstRemoveRowButtonIfOnlyOneRow();
        return containingRowNumber;
    }

    removeRowButtonOnClick = (e) => {
        const deletedRowNumber = this.removeRow(e.currentTarget);
        this.exportTableDataToJsonAndStoreInOutputElement();
        this.updateAndExportTableRowAddAndDeleteData("delete", deletedRowNumber);
    }

    setupNewRemoveRowButton(removeRowButton) {
        removeRowButton.addEventListener("click", this.removeRowButtonOnClick);
    }

    // Load input data before page refresh/after failed form submission
    loadPreviousData() {
        // Implemented in child classes
    }
}