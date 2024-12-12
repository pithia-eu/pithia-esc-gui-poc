import {
    CatalogueDataSubsetSourcesTab,
} from "/static/metadata_editor/components/catalogue_data_subset/catalogue_data_subset_sources_tab.js";


class CatalogueDataSubsetUpdateSourcesTab extends CatalogueDataSubsetSourcesTab {
    setFileUploadDisplayState(isDisplayed, isRequiredAttributeUpdated, fileInputArea) {
        const fileInput = fileInputArea.querySelector("input[type='file']");
        // Enable/disable file input
        fileInput.disabled = !isDisplayed;

        // Show/hide file input
        if (isDisplayed) {
            fileInputArea.classList.remove("d-none");
        } else {
            fileInputArea.classList.add("d-none");
        }

        if (!isRequiredAttributeUpdated) {
            return;
        }

        // Update file input required attribute
        // if needed.
        if (isDisplayed) {
            fileInput.required = true;
        } else {
            fileInput.removeAttribute("required");
        }
    }

    configureFileInputsIfExistingDataHubFileForTabPane(tabPane) {
        const useExistingSourceFileCheckbox = tabPane.querySelector("input[name='is_existing_datahub_file_used']");
        const fileUploadArea = tabPane.querySelector(".source-file-option");
        if (!useExistingSourceFileCheckbox) {
            return this.setFileUploadDisplayState(true, false, fileUploadArea);
        }
        this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, !useExistingSourceFileCheckbox.checked, fileUploadArea);
    }

    disableExtraDataHubConfigurationOptionsForTabPane(tabPane) {
        const sourceFileOptionsFieldset = tabPane.querySelector(".source-file-options-fieldset");
        sourceFileOptionsFieldset.querySelector("legend").classList.add("visually-hidden");
        const useExistingSourceFileCheckboxWrapper = tabPane.querySelector(".existing-datahub-file-checkbox-wrapper");
        useExistingSourceFileCheckboxWrapper.remove();
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        super.updateTabPaneConditionalRequiredFieldStates(tabPane);
        this.configureFileInputsIfExistingDataHubFileForTabPane(tabPane);
    }

    tabPaneControlEventHandlerActions(tabPane) {
        super.tabPaneControlEventHandlerActions(tabPane);
        this.updateTabPaneConditionalRequiredFieldStates(tabPane);
    }

    createTabOnClickActions(newTabPane) {
        this.disableExtraDataHubConfigurationOptionsForTabPane(newTabPane);
        super.createTabOnClickActions();
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
        // If a source file is in DataHub,
        // provide options to continue using
        // the file or to upload a new file.
        console.log("source", source);
        console.log("source.isSourceFileInDataHub", source.isSourceFileInDataHub);
        if (source.isSourceFileInDataHub) {
            // Update file input element label
            const fileUploadArea = correspondingTabPane.querySelector(".source-file-option");
            const fileUploadElement = fileUploadArea.querySelector("input[type='file']");
            const fileUploadLabel = fileUploadArea.querySelector(`label[for='${fileUploadElement.id}']`);
            fileUploadLabel.textContent = "Upload a New File";
            
            // Set existing file usage checkbox
            const useExistingSourceFileCheckbox = correspondingTabPane.querySelector("input[name='is_existing_datahub_file_used']");
            useExistingSourceFileCheckbox.checked = source.isExistingDataHubFileUsed;
            useExistingSourceFileCheckbox.addEventListener("change", () => {
                this.configureFileInputsIfExistingDataHubFileForTabPane(correspondingTabPane);
            });
            return this.configureFileInputsIfExistingDataHubFileForTabPane(correspondingTabPane);            
        }

        // If a source file is not in DataHub,
        // only allow uploading a new file.
        this.disableExtraDataHubConfigurationOptionsForTabPane(correspondingTabPane);
    }
}

export function setupCatalogueDataSubsetUpdateSourcesTab() {
    const sourcesTab = new CatalogueDataSubsetUpdateSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}