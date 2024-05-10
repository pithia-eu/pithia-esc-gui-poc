import {
    DynamicEditorTable,
} from "/static/register_with_support/components/table_utils.js";

class CapabilityLinkTimeSpansTable extends DynamicEditorTable {
    
}

export function setupCapabilityLinkTimeSpansTable() {
    const timeSpansTable = new CapabilityLinkTimeSpansTable();
    timeSpansTable.setup();
    return timeSpansTable;
}