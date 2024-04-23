const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

export function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
}

export class DynamicEditorTable {
    constructor(tableSelector, tableBodySelector, addRowButtonSelector, removeRowButtonSelector, rowContentTemplateSelector, jsonOutputSelector) {
        this.table = document.querySelector(tableSelector);
        this.tableBody = document.querySelector(tableBodySelector);
        this.rowContentTemplate = JSON.parse(document.querySelector(rowContentTemplateSelector).textContent);
        this.addRowButton = document.querySelector(addRowButtonSelector);
        this.removeRowButtonSelector = removeRowButtonSelector;
        this.jsonOutputElement = document.querySelector(jsonOutputSelector);
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

    // JSON export
    exportTableData() {
        // Implemented in child class
    }

    exportTableDataToJsonAndStoreInOutputElement() {
        const tableExportData = JSON.stringify(this.exportTableData());
        this.jsonOutputElement.value = tableExportData;
    }

    // New row setup
    setupDuplicatedContentInNewRow(newRow) {
        const removeRowButton = newRow.querySelector(this.removeRowButtonSelector);
        removeRowButton.disabled = false;

        // Ensure the any element IDs in the
        // row content template are unique.
        const childElementsWithIdAttribute = newRow.querySelectorAll("[id]");
        childElementsWithIdAttribute.forEach(elem => {
            const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
            const correspondingLabels = newRow.querySelectorAll(`label[for="${elem.id}"]`);
            const correspondingAriaDescBys = newRow.querySelectorAll(`[aria-describedby="${elem.id}"]`);
            elem.id = newId;
            correspondingLabels.forEach(label => {
                label.htmlFor = newId;
            });
            correspondingAriaDescBys.forEach(elem => {
                elem.setAttribute("aria-describedby", newId);
            });
        });
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
    }

    setupAddRowButton() {
        this.addRowButton.addEventListener("click", this.addRowButtonOnClick);
    }

    // Row removal
    removeRow(rowChildNode) {
        const containingRow = this.getParentRowOfChildNode(rowChildNode);
        this.tableBody.removeChild(containingRow);
        this.disableFirstRemoveRowButtonIfOnlyOneRow();
    }

    removeRowButtonOnClick = (e) => {
        this.removeRow(e.currentTarget);
        this.exportTableDataToJsonAndStoreInOutputElement();
    }

    setupNewRemoveRowButton(removeRowButton) {
        removeRowButton.addEventListener("click", this.removeRowButtonOnClick);
    }

    // Load input data before page refresh/after failed form submission
    loadPreviousData() {
        // Implemented in child classes
    }
}