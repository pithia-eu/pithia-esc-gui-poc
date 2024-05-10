import {
    DynamicEditorTab,
} from "/static/register_with_support/components/tab_utils.js";
import {
    CapabilityLinkStandardIdentifiersTable,
} from "/static/register_with_support/components/acquisition_and_computation/capability_link_standard_identifiers_table.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";


class CapabilityLinksTab extends DynamicEditorTab {
    constructor() {
        super(
            "#capability-links-tab",
            "#capability-links-tab-content",
            "#capability-links-tab-pane-content-template",
            ".remove-capability-link-button",
            "input[name='capability_links_json']",
            "Capability Link"
        );
    }

    setup() {
        super.setup();
        const firstTabPane = this.tabContent.querySelector(".tab-pane");
        this.standardIdentifiersTable = new CapabilityLinkStandardIdentifiersTable(firstTabPane.id);
        this.standardIdentifiersTable.setup();
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        const inputs = tabPane.querySelectorAll("input");
        const selects = tabPane.querySelectorAll("select");
    
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                this.exportTabData();
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                this.exportTabData();
            });
        });
    }

    getTabDataAsJson() {
        const capabilityLinks = [];
        const capabilityLinkTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        capabilityLinkTabPanes.forEach(tabPane => {
            capabilityLinks.push({
                platform: tabPane.querySelector("select[name='capability_link_platform']").value,
                acquisitionCapabilities: tabPane.querySelector("select[name='capability_link_platform']").value,
                standardIdentifiers: tabPane.querySelector("input[name='capability_link_standard_identifiers_json']").value,
                timeSpans: tabPane.querySelector("input[name='capability_link_standard_identifiers_json']").value,
            });
        });
        return capabilityLinks;
    }

    loadPreviousTabData() {
        
    }
}

export function setupCapabilityLinksTab() {
    const capabilityLinksTab = new CapabilityLinksTab();
    capabilityLinksTab.setup();
    return capabilityLinksTab;
}