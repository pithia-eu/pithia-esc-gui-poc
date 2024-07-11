import {
    StandardIdentifiersTable,
} from "/static/metadata_editor/components/standard_identifiers_table.js";


class PlatformStandardIdentifiersTable extends StandardIdentifiersTable {
    constructor() {
        super(
            "#table-standard-identifiers",
            "#table-standard-identifiers tbody",
            "#add-sirow-button",
            ".remove-sirow-button",
            "#standard-identifier-row-content-template",
            "input[name='standard_identifiers_json']",
            "input[name='standard_identifier_authority']",
            "input[name='standard_identifier']",
        );
    }
}

export function setupPlatformStandardIdentifiersTable() {
    const newStandardIdentifiersTable = new PlatformStandardIdentifiersTable();
    newStandardIdentifiersTable.setup();
    return newStandardIdentifiersTable;
}