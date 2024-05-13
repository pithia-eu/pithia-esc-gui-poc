import {
    StandardIdentifiersTable,
} from "/static/register_with_support/components/standard_identifiers_table.js";

export class CapabilityLinkStandardIdentifiersTable extends StandardIdentifiersTable {
    constructor(tabId) {
        super(
            `#${tabId} .table-standard-identifiers`,
            `#${tabId} .table-standard-identifiers tbody`,
            `#${tabId} .add-sirow-button`,
            `.remove-clsirow-button`,
            `#capability-link-standard-identifier-row-content-template`,
            `#${tabId} input[name='capability_link_standard_identifiers_json']`,
            `input[name='capability_link_standard_identifier_authority']`,
            `input[name='capability_link_standard_identifier']`,
        );
    }

    exportTableDataToJsonAndStoreInOutputElement() {
        super.exportTableDataToJsonAndStoreInOutputElement();
        const inputEvent = new Event("input", {
            bubbles: true,
        });
        this.jsonOutputElement.dispatchEvent(inputEvent);
    }
}