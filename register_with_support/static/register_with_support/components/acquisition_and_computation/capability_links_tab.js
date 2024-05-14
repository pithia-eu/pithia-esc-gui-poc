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

const requiredFieldSelector = "select[name='capability_link_acquisition_capabilities']";


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
        const inputs = Array.from(tabPane.querySelectorAll("input"));
        const selects = Array.from(tabPane.querySelectorAll("select"));
        const allTabPaneFields = [
            ...inputs,
            ...selects,
        ];
    
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                checkAndSetRequiredAttributesForFields(
                    tabPane.querySelectorAll(requiredFieldSelector),
                    allTabPaneFields,
                );
                this.exportTabData();
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                checkAndSetRequiredAttributesForFields(
                    tabPane.querySelectorAll(requiredFieldSelector),
                    allTabPaneFields,
                );
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
            capabilityLinks.push({
                platforms: platformSelectedOptions.map(option => option.value),
                acquisitionCapabilities: tabPane.querySelector("select[name='capability_link_acquisition_capabilities']").value,
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
                const correspondingOption = platformSelect.querySelector(`option[value="${platform}"]`);
                if (correspondingOption) {
                    correspondingOption.selected = true;
                }
            });
            correspondingTabPane.querySelector("select[name='capability_link_acquisition_capabilities']").value = capabilityLink.acquisitionCapabilities;
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
            checkAndSetRequiredAttributesForFields(
                correspondingTabPane.querySelectorAll(requiredFieldSelector),
                [
                    ...Array.from(correspondingTabPane.querySelectorAll("input")),
                    ...Array.from(correspondingTabPane.querySelectorAll("select")),
                ],
            );
        });
    }
}

export function setupCapabilityLinksTab() {
    const capabilityLinksTab = new CapabilityLinksTab();
    capabilityLinksTab.setup();
    return capabilityLinksTab;
}