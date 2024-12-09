import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    SourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";


export class CatalogueDataSubsetSourcesTab extends SourcesTab {
    constructor() {
        super();
        this.sourceLinkageInputWrapperSelector = ".source-linkage-wrapper";
        this.sourceFileInputSelector = "input[type='file']";
        this.sourceFileInputWrapperSelector = ".source-file-wrapper";
    }

    enableSourceFileSharingMethod(inputWrapperSelector) {
        const inputWrappersInTab = this.tabContent.querySelectorAll(inputWrapperSelector);
        for (const inputWrapper of inputWrappersInTab) {
            const inputsInWrapper = inputWrapper.querySelectorAll("input");
            for (const input of inputsInWrapper) {
                input.disabled = true;
            }
            inputWrapper.classList.add("d-none");
        }
    }

    disableSourceFileSharingMethod(inputWrapperSelector) {
        const inputWrappersInTab = this.tabContent.querySelectorAll(inputWrapperSelector);
        for (const inputWrapper of inputWrappersInTab) {
            const inputsInWrapper = inputWrapper.querySelectorAll("input");
            for (const input of inputsInWrapper) {
                input.disabled = false;
            }
            inputWrapper.classList.remove("d-none");
        }
    }
    
    setSourceFileSharingMethodToLinkage() {
        this.enableSourceFileSharingMethod(this.sourceLinkageInputWrapperSelector);
        this.disableSourceFileSharingMethod(this.sourceFileInputWrapperSelector);
    }
    
    setSourceFileSharingMethodToFileUpload() {
        this.enableSourceFileSharingMethod(this.sourceFileInputWrapperSelector);
        this.disableSourceFileSharingMethod(this.sourceLinkageInputWrapperSelector);
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        // Required fields
        const requiredFieldSelectorsUnformatted = [
            this.sourceFileInputSelector,
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

    createTabPane(newTabIdPrefix) {
        const newTabPane = super.createTabPane(newTabIdPrefix);
        const sourceFileInput = newTabPane.querySelector("input[name='source_file']");
        sourceFileInput.setAttribute("name", `${sourceFileInput.name}_${this.nextTabNumber}`);
        return newTabPane;
    }

    tabPaneControlEventHandlerActions(tabPane) {
        super.tabPaneControlEventHandlerActions(tabPane);
        this.updateTabPaneConditionalRequiredFieldStates(tabPane);
    }

    getTabPaneData(tabPane) {
        const tabPaneData = super.getTabPaneData(tabPane);
        tabPaneData.fileInputName = tabPane.querySelector("input[type='file']").name;
        return tabPaneData;
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
        const tabPanes = this.tabContent.querySelectorAll(".tab-pane");
        tabPanes.forEach(tabPane => {
            this.updateTabPaneConditionalRequiredFieldStates(tabPane);
        });
    }
}

export function setupCatalogueDataSubsetSourcesTab() {
    const sourcesTab = new CatalogueDataSubsetSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}