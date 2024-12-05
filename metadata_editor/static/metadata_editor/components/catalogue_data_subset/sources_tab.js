import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    SourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";


class CatalogueDataSubsetSourcesTab extends SourcesTab {
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