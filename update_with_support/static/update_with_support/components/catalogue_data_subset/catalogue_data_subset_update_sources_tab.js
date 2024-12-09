import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    CatalogueDataSubsetSourcesTab,
} from "/static/metadata_editor/components/catalogue_data_subset/catalogue_data_subset_sources_tab.js";


class CatalogueDataSubsetUpdateSourcesTab extends CatalogueDataSubsetSourcesTab {
    setFileUploadDisplayState(isDisplayed, fileInputArea) {
        if (isDisplayed) {
            return fileInputArea.classList.remove("d-none");
        }
        return fileInputArea.classList.add("d-none");
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

    tabPaneControlEventHandlerActions(tabPane) {
        super.tabPaneControlEventHandlerActions(tabPane);
        this.updateTabPaneConditionalRequiredFieldStates(tabPane);
    }

    getTabPaneData(tabPane) {
        const tabPaneData = super.getTabPaneData(tabPane);
        const existingDataHubFileCheckbox = tabPane.querySelector("input[name='is_existing_datahub_file_used']");
        if (!existingDataHubFileCheckbox) {
            tabPaneData.isExistingDataHubFileUsed = false;
            return tabPaneData;
        }
        tabPaneData.isExistingDataHubFileUsed = existingDataHubFileCheckbox.checked;
        return tabPaneData;
    }

    loadPreviousTabPaneData(source, correspondingTabPane) {
        super.loadPreviousTabPaneData(source, correspondingTabPane);
        // File
        const sourceFileOptionsFieldset = correspondingTabPane.querySelector(".source-file-options-fieldset");
        const useExistingSourceFileCheckboxWrapper = sourceFileOptionsFieldset.querySelector(".existing-datahub-file-checkbox-wrapper");
        const useExistingSourceFileCheckbox = useExistingSourceFileCheckboxWrapper.querySelector("input[type='checkbox']");
        // If a source file is in DataHub,
        // provide options to continue using
        // the file or to upload a new file.
        if (source.isSourceFileInDataHub) {
            // Update file input element label
            const fileUploadArea = correspondingTabPane.querySelector(".source-file-option");
            const fileUploadElement = fileUploadArea.querySelector("input[type='file']");
            const fileUploadLabel = fileUploadArea.querySelector(`label[for='${fileUploadElement.id}']`);
            fileUploadLabel.textContent = "Upload a New File";

            // Set existing file usage checkbox
            useExistingSourceFileCheckbox.checked = source.isExistingDataHubFileUsed;
            useExistingSourceFileCheckbox.addEventListener("change", () => {
                this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, fileUploadArea);
            });
            this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, fileUploadArea);
            return;
        }

        // If a source file is not in DataHub,
        // only allow uploading a new file.
        sourceFileOptionsFieldset.querySelector("legend").classList.add("visually-hidden");
        useExistingSourceFileCheckboxWrapper.remove();
    }
}

export function setupCatalogueDataSubsetUpdateSourcesTab() {
    const sourcesTab = new CatalogueDataSubsetUpdateSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}