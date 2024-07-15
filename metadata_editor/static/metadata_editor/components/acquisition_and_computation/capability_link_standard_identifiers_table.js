import {
    StandardIdentifiersTable,
} from "/static/metadata_editor/components/standard_identifiers_table.js";

export class CapabilityLinkStandardIdentifiersTable extends StandardIdentifiersTable {
    constructor(tabId) {
        super(
            `#${tabId} .table-standard-identifiers`,
            `#${tabId} .table-standard-identifiers tbody`,
            `#${tabId} .add-sirow-button`,
            `.remove-clsirow-button`,
            `#capability-link-standard-identifier-row-content-template`,
            `#${tabId} input[name='capability_link_standard_identifiers_json']`,
            `#${tabId} input[name='capability_link_standard_identifiers_extra_json']`,
            `input[name='capability_link_standard_identifier_authority']`,
            `input[name='capability_link_standard_identifier']`,
        );
    }

    addRow() {
        const newRow = super.addRow();

        this.table.dispatchEvent(new CustomEvent("newTableRowInputsAdded", {
            detail: {
                inputIds: Array.from(newRow.querySelectorAll("input")).map(el => el.id),
                selectIds: Array.from(newRow.querySelectorAll("select")).map(el => el.id),
            },
        }));
    }

    exportTableDataToJsonAndStoreInOutputElement() {
        super.exportTableDataToJsonAndStoreInOutputElement();
        const inputEvent = new Event("input", {
            bubbles: true,
        });
        this.jsonOutputElement.dispatchEvent(inputEvent);
    }
}