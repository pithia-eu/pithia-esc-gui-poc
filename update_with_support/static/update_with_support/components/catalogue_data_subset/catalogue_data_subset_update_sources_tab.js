import {
    CatalogueDataSubsetSourcesTab,
} from "/static/metadata_editor/components/catalogue_data_subset/catalogue_data_subset_sources_tab.js";


class CatalogueDataSubsetUpdateSourcesTab extends CatalogueDataSubsetSourcesTab {
    setFileUploadDisplayState(isDisplayed, isRequiredAttributeUpdated, fileInputWrapper) {
        const fileInput = fileInputWrapper.querySelector("input[type='file']");
        // Enable/disable file input
        fileInput.disabled = !isDisplayed;

        // Show/hide file input
        if (isDisplayed) {
            fileInputWrapper.classList.remove("d-none");
        } else {
            fileInputWrapper.classList.add("d-none");
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
        const fileInputWrapper = tabPane.querySelector(".source-file-option");
        if (!useExistingSourceFileCheckbox) {
            return this.setFileUploadDisplayState(true, false, fileInputWrapper);
        }
        this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, !useExistingSourceFileCheckbox.checked, fileInputWrapper);
    }

    disableExtraDataHubConfigurationOptionsForTabPane(tabPane) {
        const sourceFileOptionsFieldset = tabPane.querySelector(".source-file-options-fieldset");
        // Hide file option fieldset, but keep legend accessible.
        sourceFileOptionsFieldset.querySelector("legend").classList.add("visually-hidden");
        // Remove extra datahub management features as they
        // shouldn't be needed.
        const dataHubManagementElementsWrapper = tabPane.querySelector(".existing-datahub-file-checkbox-wrapper");
        dataHubManagementElementsWrapper.remove();
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
        const dataHubManagementElementsWrapper = tabPane.querySelector(".existing-datahub-file-checkbox-wrapper");
        if (!dataHubManagementElementsWrapper) {
            tabPaneData.dataHubFileName = '';
            tabPaneData.isExistingDataHubFileUsed = false;
            return tabPaneData;
        }
        const dataHubFileNameHiddenInput = tabPane.querySelector("input[name='source_datahub_file_name']");
        const existingDataHubFileCheckbox = tabPane.querySelector("input[name='is_existing_datahub_file_used']");
        tabPaneData.dataHubFileName = dataHubFileNameHiddenInput.value;
        tabPaneData.isExistingDataHubFileUsed = existingDataHubFileCheckbox.checked;
        return tabPaneData;
    }

    loadPreviousTabPaneData(source, correspondingTabPane) {
        super.loadPreviousTabPaneData(source, correspondingTabPane);
        // File
        // If a source file is in DataHub,
        // provide options to continue using
        // the file or to upload a new file.
        if (source.dataHubFileName) {
            // Update file input element label
            const fileInputWrapper = correspondingTabPane.querySelector(".source-file-option");
            const fileInputElement = fileInputWrapper.querySelector("input[type='file']");
            const fileInputLabel = fileInputWrapper.querySelector(`label[for='${fileInputElement.id}']`);
            fileInputLabel.textContent = "Upload a New File";
            
            // Set hidden datahub file name input
            const dataHubFileNameHiddenInput = correspondingTabPane.querySelector("input[name='source_datahub_file_name']");
            dataHubFileNameHiddenInput.value = source.dataHubFileName;

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