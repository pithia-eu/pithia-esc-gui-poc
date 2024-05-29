import {
    DynamicEditorTab,
} from "/static/register_with_support/components/tab_utils.js";
import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/register_with_support/components/conditional_required_fields.js";


class SourcesTab extends DynamicEditorTab {
    constructor() {
        super(
            "#sources-tab",
            "#sources-tab-content",
            "#sources-tab-pane-content-template",
            ".remove-source-button",
            "input[name='sources_json']",
            "Source"
        );
        this.sourceServiceFunctionSelectSelector = "select[name='source_service_function']";
        this.sourceLinkageInputSelector = "input[name='source_linkage']";
        this.sourceProtocolInputSelector = "input[name='source_protocol']";
        this.sourceNameInputSelector = "input[name='source_name']";
        this.sourceDescriptionTextareaSelector = "textarea[name='source_description']";
        this.sourceDataFormatSelectSelector = "select[name='source_data_formats']";
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        // Required fields
        const requiredFieldSelectorsUnformatted = [
            this.sourceLinkageInputSelector,
            this.sourceNameInputSelector,
            this.sourceProtocolInputSelector,
        ];
        
        // Optional related fields that affect
        // whether the required field attributes
        // for conditional required fields are
        // set.
        const optionalFieldSelectorsUnformatted = [
            this.sourceServiceFunctionSelectSelector,
            this.sourceDescriptionTextareaSelector,
            this.sourceDataFormatSelectSelector,
        ];
        checkAndSetRequiredAttributesForFieldsBySelectors(
            requiredFieldSelectorsUnformatted.map(selector => `#${tabPane.id} ${selector}`).join(", "),
            optionalFieldSelectorsUnformatted.map(selector => `#${tabPane.id} ${selector}`).join(", "),
        );
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        const inputs = Array.from(tabPane.querySelectorAll("input"));
        const selects = Array.from(tabPane.querySelectorAll("select"));
        const textareas = Array.from(tabPane.querySelectorAll("textarea"));
    
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
                this.exportTabData();
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
                this.exportTabData();
            });
        });

        textareas.forEach(textarea => {
            textarea.addEventListener("input", () => {
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
                this.exportTabData();
            });
        });
    }

    getTabDataAsJson() {
        const sources = [];
        const sourceTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        sourceTabPanes.forEach(tabPane => {
            const serviceFunctionSelect = tabPane.querySelector(this.sourceServiceFunctionSelectSelector);
            const linkageInput = tabPane.querySelector(this.sourceLinkageInputSelector);
            const nameInput = tabPane.querySelector(this.sourceNameInputSelector);
            const protocolInput = tabPane.querySelector(this.sourceProtocolInputSelector);
            const descriptionTextarea = tabPane.querySelector(this.sourceDescriptionTextareaSelector);
            const dataFormatSelect = tabPane.querySelector(this.sourceDataFormatSelectSelector);
            const dataFormatSelectedOptions = Array.from(dataFormatSelect.selectedOptions);
            sources.push({
                serviceFunction: serviceFunctionSelect.value,
                linkage: linkageInput.value,
                name: nameInput.value,
                protocol: protocolInput.value,
                description: descriptionTextarea.value,
                dataFormats: dataFormatSelectedOptions.map(option => option.value),
            });
        });
        return sources;
    }

    loadPreviousTabData() {
        const previousSources = JSON.parse(this.jsonExportElement.value);
        if (!previousSources) {
            return;
        }
        previousSources.forEach((source, i) => {
            if (i !== 0) {
                this.createTabAndTabPane();
            }
            const correspondingTabPane = this.tabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
            
            // Service function
            const serviceFunctionSelect = correspondingTabPane.querySelector(this.sourceServiceFunctionSelectSelector);
            serviceFunctionSelect.value = source.serviceFunction;
            
            // Linkage
            const linkageInput = correspondingTabPane.querySelector(this.sourceLinkageInputSelector);
            linkageInput.value = source.linkage;

            // Name
            const nameInput = correspondingTabPane.querySelector(this.sourceNameInputSelector);
            nameInput.value = source.name;

            // Protocol
            const protocolInput = correspondingTabPane.querySelector(this.sourceProtocolInputSelector);
            protocolInput.value = source.protocol;

            // Description
            const descriptionTextarea = correspondingTabPane.querySelector(this.sourceDescriptionTextareaSelector);
            descriptionTextarea.value = source.description;

            // Data formats
            const dataFormatSelect = correspondingTabPane.querySelector(this.sourceDataFormatSelectSelector);
            dataFormatSelect.value = "";
            source.dataFormats.forEach(dataFormat => {
                const correspondingOption = dataFormatSelect.querySelector(`option[value="${dataFormat}"]`);
                if (correspondingOption) {
                    correspondingOption.selected = true;
                }
            });
            const selects = correspondingTabPane.querySelectorAll("select:not(table select)");
            if (selects) {
                selects.forEach(select => { 
                    window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                        detail: select.id,
                    }));
                });
            }
            this.updateTabPaneConditionalRequiredFieldStates(correspondingTabPane);
        });
    }
}

export function setupSourcesTab() {
    const sourcesTab = new SourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}