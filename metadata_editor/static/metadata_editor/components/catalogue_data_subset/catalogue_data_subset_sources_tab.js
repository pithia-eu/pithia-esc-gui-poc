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
        this.enabledSourceFileSharingMethodInputSelector = this.sourceFileInputSelector;
        this.enabledSourceFileSharingMethodInputWrapperSelector = this.sourceFileInputWrapperSelector;
        this.disabledSourceFileSharingMethodInputSelector = this.sourceLinkageInputSelector;
        this.disabledSourceFileSharingMethodInputWrapperSelector = this.sourceLinkageInputWrapperSelector;
    }

    enableSourceFileSharingMethodForTabPane(tabPane, inputWrapperSelector) {
        const inputWrappersInTab = tabPane.querySelectorAll(inputWrapperSelector);
        for (const inputWrapper of inputWrappersInTab) {
            const inputsInWrapper = inputWrapper.querySelectorAll("input");
            for (const input of inputsInWrapper) {
                input.disabled = false;
            }
            inputWrapper.classList.remove("d-none");
        }
    }

    disableSourceFileSharingMethodForTabPane(tabPane, inputWrapperSelector) {
        const inputWrappersInTab = tabPane.querySelectorAll(inputWrapperSelector);
        for (const inputWrapper of inputWrappersInTab) {
            const inputsInWrapper = inputWrapper.querySelectorAll("input");
            for (const input of inputsInWrapper) {
                input.disabled = true;
            }
            inputWrapper.classList.add("d-none");
        }
    }

    applySourceFileSharingMethodChoiceToTabPane(tabPane) {
        this.enableSourceFileSharingMethodForTabPane(tabPane, this.enabledSourceFileSharingMethodInputWrapperSelector);
        this.disableSourceFileSharingMethodForTabPane(tabPane, this.disabledSourceFileSharingMethodInputWrapperSelector);
    }

    applySourceFileSharingMethodChoiceToAllTabPanes() {
        const tabPanes = this.tabContent.querySelectorAll(".tab-pane");
        for (const tabPane of tabPanes) {
            this.applySourceFileSharingMethodChoiceToTabPane(tabPane);
        }
    }

    setSourceFileSharingMethodToLinkage() {
        this.enabledSourceFileSharingMethodInputSelector = this.sourceLinkageInputSelector;
        this.enabledSourceFileSharingMethodInputWrapperSelector = this.sourceLinkageInputWrapperSelector;
        this.disabledSourceFileSharingMethodInputSelector = this.sourceFileInputSelector;
        this.disabledSourceFileSharingMethodInputWrapperSelector = this.sourceFileInputWrapperSelector;
        this.applySourceFileSharingMethodChoiceToAllTabPanes();
    }
    
    setSourceFileSharingMethodToFileUpload() {
        this.enabledSourceFileSharingMethodInputSelector = this.sourceFileInputSelector;
        this.enabledSourceFileSharingMethodInputWrapperSelector = this.sourceFileInputWrapperSelector;
        this.disabledSourceFileSharingMethodInputSelector = this.sourceLinkageInputSelector;
        this.disabledSourceFileSharingMethodInputWrapperSelector = this.sourceLinkageInputWrapperSelector;
        this.applySourceFileSharingMethodChoiceToAllTabPanes();
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        // Required fields
        const requiredFieldSelectorsUnformatted = [
            this.enabledSourceFileSharingMethodInputSelector,
            this.sourceNameInputSelector,
            this.sourceProtocolInputSelector,
        ];
        
        // Optional related fields that affect
        // whether the required field attributes
        // for conditional required fields are
        // set.
        const optionalFieldSelectorsUnformatted = [
            this.disabledSourceFileSharingMethodInputSelector,
            this.sourceServiceFunctionSelectSelector,
            this.sourceDescriptionTextareaSelector,
            this.sourceDataFormatSelectSelector,
        ];
        checkAndSetRequiredAttributesForFieldsBySelectors(
            requiredFieldSelectorsUnformatted.map(selector => `#${tabPane.id} ${selector}`).join(", "),
            optionalFieldSelectorsUnformatted.map(selector => `#${tabPane.id} ${selector}`).join(", "),
        );
    }

    updateAllTabPaneConditionalRequiredFieldStates() {
        const tabPanes = this.tabContent.querySelectorAll(".tab-pane");
        tabPanes.forEach(tabPane => {
            this.updateTabPaneConditionalRequiredFieldStates(tabPane);
        });
    }

    createTabPane(newTabIdPrefix) {
        const newTabPane = super.createTabPane(newTabIdPrefix);
        const sourceFileInput = newTabPane.querySelector("input[name='source_file']");
        sourceFileInput.setAttribute("name", `${sourceFileInput.name}_${this.nextTabNumber}`);
        this.applySourceFileSharingMethodChoiceToTabPane(newTabPane);
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
        this.updateAllTabPaneConditionalRequiredFieldStates();
    }
}

export function setupCatalogueDataSubsetSourcesTab() {
    const sourcesTab = new CatalogueDataSubsetSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}