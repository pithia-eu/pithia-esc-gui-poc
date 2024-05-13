import {
    DynamicEditorTab,
} from "/static/register_with_support/components/tab_utils.js";
import {
    CapabilityLinkStandardIdentifiersTable,
} from "/static/register_with_support/components/acquisition_and_computation/capability_link_standard_identifiers_table.js";
import {
    CapabilityLinkTimeSpansTable,
} from "/static/register_with_support/components/acquisition_and_computation/capability_link_time_spans_table.js";
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
        this.timeSpansTable = new CapabilityLinkTimeSpansTable(firstTabPane.id);
        this.timeSpansTable.setup();
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

    createTabOnClickActions(newTabPane) {
        const standardIdentifiersTable = new CapabilityLinkStandardIdentifiersTable(newTabPane.id);
        standardIdentifiersTable.setup();
        const timeSpansTable = new CapabilityLinkTimeSpansTable(newTabPane.id);
        timeSpansTable.setup();
    }

    getTabDataAsJson() {
        const capabilityLinks = [];
        const capabilityLinkTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        capabilityLinkTabPanes.forEach(tabPane => {
            const platformSelect = tabPane.querySelector("select[name='capability_link_platform']");
            const platformSelectedOptions = Array.from(platformSelect.selectedOptions);
            const acquisitioniCapabilitiesSelect = tabPane.querySelector("select[name='capability_link_platform']");
            const acquisitionCapabilitiesSelectedOptions = Array.from(acquisitioniCapabilitiesSelect.selectedOptions);
            capabilityLinks.push({
                platforms: platformSelectedOptions.map(option => option.value),
                acquisitionCapabilities: acquisitionCapabilitiesSelectedOptions.map(option => option.value),
                standardIdentifiers: tabPane.querySelector("input[name='capability_link_standard_identifiers_json']").value,
                timeSpans: tabPane.querySelector("input[name='capability_link_time_spans_json']").value,
            });
        });
        return capabilityLinks;
    }

    loadPreviousTabData() {
        const previousCapabilityLinks = JSON.parse(this.jsonExportElement.value);
        if (!previousCapabilityLinks) {
            return;
        }
        previousCapabilityLinks.forEach((capabilityLink, i) => {
            if (i !== 0) {
                this.createTabAndTabPane();
            }
            const correspondingTabPane = this.tabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
            const platformSelect = correspondingTabPane.querySelector("select[name='capability_link_platform']");
            platformSelect.value = "";
            capabilityLink.platforms.forEach(platform => {
                platformSelect.querySelector(`option[value="${platform}"]`).selected = true;
            });
            const acquisitionCapabilitiesSelect = correspondingTabPane.querySelector("select[name='capability_link_platform']");
            acquisitionCapabilitiesSelect.value = "";
            capabilityLink.acquisitionCapabilities.forEach(ac => {
                acquisitionCapabilitiesSelect.querySelector(`option[value="${ac}"]`).selected = true;
            });
            correspondingTabPane.querySelector("input[name='capability_link_standard_identifiers_json']").value = capabilityLink.standardIdentifiers;
            correspondingTabPane.querySelector("input[name='capability_link_time_spans_json']").value = capabilityLink.timeSpans;
            if (i !== 0) {
                const standardIdentifiersTable = new CapabilityLinkStandardIdentifiersTable(correspondingTabPane.id);
                standardIdentifiersTable.setup();
                const timeSpansTable = new CapabilityLinkTimeSpansTable(correspondingTabPane.id);
                timeSpansTable.setup();
            }
            const selects = correspondingTabPane.querySelectorAll("select:not(table select)");
            if (selects) {
                selects.forEach(select => { 
                    window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                        detail: select.id,
                    }));
                });
            }

        });
    }
}

export function setupCapabilityLinksTab() {
    const capabilityLinksTab = new CapabilityLinksTab();
    capabilityLinksTab.setup();
    return capabilityLinksTab;
}