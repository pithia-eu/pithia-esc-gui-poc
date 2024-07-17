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
        this.numNewRows = 0;
        this.deletedRowIndexSequence = [];
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

    getRowIndex(row) {
        return Array.from(this.tableBody.children).indexOf(row);
    }

    // JSON export
    incrementNumberOfNewRows() {
        this.numNewRows += 1;
    }

    addRowToDeletedRowSequence(rowIndex) {
        this.deletedRowIndexSequence.push(rowIndex);
    }

    exportExtraTableDataToJsonAndStoreInOutputElement() {
        const extraTableData = {
            numAdditions: this.numNewRows,
            deletedIndexSequence: this.deletedRowIndexSequence,
        };
        this.jsonExtraOutputElement.value = JSON.stringify(extraTableData);
        window.dispatchEvent(new CustomEvent("dynamicTableDataExported"));
    }

    exportTableData() {
        // Implemented in child class
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
        this.incrementNumberOfNewRows();
        this.exportTableDataToJsonAndStoreInOutputElement();
        this.exportExtraTableDataToJsonAndStoreInOutputElement();
    }

    setupAddRowButton() {
        this.addRowButton.addEventListener("click", this.addRowButtonOnClick);
    }

    // Row removal
    removeRow(rowChildNode) {
        const containingRow = this.getParentRowOfChildNode(rowChildNode);
        const containingRowIndex = this.getRowIndex(containingRow);
        this.tableBody.removeChild(containingRow);
        this.disableFirstRemoveRowButtonIfOnlyOneRow();
        return containingRowIndex;
    }

    removeRowButtonOnClick = (e) => {
        const deletedRowIndex = this.removeRow(e.currentTarget);
        this.addRowToDeletedRowSequence(deletedRowIndex);
        this.exportTableDataToJsonAndStoreInOutputElement();
        this.exportExtraTableDataToJsonAndStoreInOutputElement();
    }

    setupNewRemoveRowButton(removeRowButton) {
        removeRowButton.addEventListener("click", this.removeRowButtonOnClick);
    }

    // Load input data before page refresh/after failed form submission
    loadPreviousData() {
        const extraTableData = JSON.parse(this.jsonExtraOutputElement.value);
        if ("numAdditions" in extraTableData) {
            this.numNewRows = parseInt(extraTableData.numAdditions);
        }
        if ("deletedIndexSequence" in extraTableData) {
            this.deletedRowIndexSequence = extraTableData.deletedIndexSequence;
        }
    }
}