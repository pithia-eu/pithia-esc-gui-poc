import {
    DynamicEditorTab,
} from "/static/metadata_editor/components/tab_utils.js";


export class SourcesTab extends DynamicEditorTab {
    constructor() {
        super(
            "#sources-tab",
            "#sources-tab-content",
            "#sources-tab-pane-content-template",
            ".remove-source-button",
            "input[name='sources_json']",
            "input[name='sources_extra_json']",
            "Online Resource"
        );
        this.sourceServiceFunctionSelectSelector = "select[name='source_service_functions']";
        this.sourceLinkageInputSelector = "input[name='source_linkage']";
        this.sourceProtocolInputSelector = "input[name='source_protocol']";
        this.sourceNameInputSelector = "input[name='source_name']";
        this.sourceDescriptionTextareaSelector = "textarea[name='source_description']";
        this.sourceDataFormatSelectSelector = "select[name='source_data_formats']";
    }

    tabPaneControlEventHandlerActions(tabPane) {
        this.exportTabData();
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        const inputs = Array.from(tabPane.querySelectorAll("input"));
        const selects = Array.from(tabPane.querySelectorAll("select"));
        const textareas = Array.from(tabPane.querySelectorAll("textarea"));
    
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                this.tabPaneControlEventHandlerActions(tabPane);
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                this.tabPaneControlEventHandlerActions(tabPane);
            });
        });

        textareas.forEach(textarea => {
            textarea.addEventListener("input", () => {
                this.tabPaneControlEventHandlerActions(tabPane);
            });
        });
    }

    getTabPaneData(tabPane) {
        const serviceFunctionSelect = tabPane.querySelector(this.sourceServiceFunctionSelectSelector);
        const serviceFunctionSelectedOptions = Array.from(serviceFunctionSelect.selectedOptions);
        const linkageInput = tabPane.querySelector(this.sourceLinkageInputSelector);
        const nameInput = tabPane.querySelector(this.sourceNameInputSelector);
        const protocolInput = tabPane.querySelector(this.sourceProtocolInputSelector);
        const descriptionTextarea = tabPane.querySelector(this.sourceDescriptionTextareaSelector);
        const dataFormatSelect = tabPane.querySelector(this.sourceDataFormatSelectSelector);
        const dataFormatSelectedOptions = Array.from(dataFormatSelect.selectedOptions);
        return {
            serviceFunctions: serviceFunctionSelectedOptions.map(option => option.value),
            linkage: linkageInput.value,
            name: nameInput.value,
            protocol: protocolInput.value,
            description: descriptionTextarea.value,
            dataFormats: dataFormatSelectedOptions.map(option => option.value),
        };
    }

    getTabDataAsJson() {
        const sources = [];
        const sourceTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        sourceTabPanes.forEach(tabPane => {
            const tabPaneData = this.getTabPaneData(tabPane);
            sources.push(tabPaneData);
        });
        return sources;
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
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
            serviceFunctionSelect.value = "";
            if ("serviceFunctions" in source) {
                source.serviceFunctions.forEach(serviceFunction => {
                    const correspondingOption = serviceFunctionSelect.querySelector(`option[value="${serviceFunction}"]`);
                    if (correspondingOption) {
                        correspondingOption.selected = true;
                    }
                });
            } else if ("serviceFunction" in source) {
                // Backwards compatibility
                serviceFunctionSelect.value = source.serviceFunction;
            }
            
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
        });
    }
}

export function setupSourcesTab() {
    const sourcesTab = new SourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}