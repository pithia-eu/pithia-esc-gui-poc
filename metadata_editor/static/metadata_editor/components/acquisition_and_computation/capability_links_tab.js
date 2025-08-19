import {
    DynamicEditorTab,
} from "/static/metadata_editor/components/tab_utils.js";
import {
    CapabilityLinkStandardIdentifiersTable,
} from "/static/metadata_editor/components/acquisition_and_computation/capability_link_standard_identifiers_table.js";
import {
    CapabilityLinkTimeSpansTable,
} from "/static/metadata_editor/components/acquisition_and_computation/capability_link_time_spans_table.js";
import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    dispatchValidateFieldsEvent,
} from "/static/metadata_editor/components/validation/utils/events.js";


function updateTabPaneConditionalRequiredFieldStates(tabPane) {
    // Required fields
    const requiredFieldSelector = "select[name='capability_link_capabilities']";
    
    // Optional related fields that affect
    // whether the required field attributes
    // for conditional required fields are
    // set.
    const platformSelectSelector = `#${tabPane.id} select[name='capability_link_platform']`;
    const standardIdentifiersTableFieldsSelector = `#${tabPane.id} input[name='capability_link_standard_identifier_authority'], #${tabPane.id} input[name='capability_link_standard_identifier']`;
    const timeSpansTableFieldsSelector = `#${tabPane.id} input[name='capability_link_time_span_begin_position'], #${tabPane.id} select[name='capability_link_time_span_end_position']`;
    const optionalRelatedFieldsSelector = `${platformSelectSelector}, ${standardIdentifiersTableFieldsSelector}, ${timeSpansTableFieldsSelector}`;
    checkAndSetRequiredAttributesForFieldsBySelectors(
        `#${tabPane.id} ${requiredFieldSelector}`,
        optionalRelatedFieldsSelector,
    );
}

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
                updateTabPaneConditionalRequiredFieldStates(tabPane);
                this.exportTabData();
                if (allTabPaneFields.some(field => field.required)) {
                    return dispatchValidateFieldsEvent([input]);
                }
                return dispatchValidateFieldsEvent(allTabPaneFields);
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                updateTabPaneConditionalRequiredFieldStates(tabPane);
                this.exportTabData();
                if (allTabPaneFields.some(field => field.required)) {
                    return dispatchValidateFieldsEvent([select]);
                }
                return dispatchValidateFieldsEvent(allTabPaneFields);
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
                capabilities: tabPane.querySelector("select[name='capability_link_capabilities']").value,
                standardIdentifiers: tabPane.querySelector("input[name='capability_link_standard_identifiers_json']").value,
                timeSpans: tabPane.querySelector("input[name='capability_link_time_spans_json']").value,
            });
        });
        return capabilityLinks;
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
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
            correspondingTabPane.querySelector("select[name='capability_link_capabilities']").value = capabilityLink.capabilities;
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
            updateTabPaneConditionalRequiredFieldStates(correspondingTabPane);
        });
    }
}

export function setupCapabilityLinksTab() {
    const capabilityLinksTab = new CapabilityLinksTab();
    capabilityLinksTab.setup();
    return capabilityLinksTab;
}