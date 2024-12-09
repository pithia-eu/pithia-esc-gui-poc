import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    SourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";


class CatalogueDataSubsetSourcesTab extends SourcesTab {
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
        if (!sourceFileOptionsFieldset) {
            return;
        }

        // If a source file is in DataHub,
        // provide options to continue using
        // the file or to upload a new file.
        if (source.isSourceFileInDataHub) {
            const dataHubFileDefault = correspondingTabPane.querySelector(".datahub-file-default");
            dataHubFileDefault.remove();

            // Update file input element label
            const fileUploadArea = correspondingTabPane.querySelector(".new-source-file-option");
            const fileUploadElement = fileUploadArea.querySelector("input[type='file']");
            const fileUploadLabel = fileUploadArea.querySelector(`label[for='${fileUploadElement.id}']`);
            fileUploadLabel.textContent = "Upload a New File";

            // Set existing file usage checkbox
            const useExistingSourceFileCheckbox = sourceFileOptionsFieldset.querySelector("input[name='is_existing_datahub_file_used']");
            useExistingSourceFileCheckbox.checked = source.isExistingDataHubFileUsed;
            useExistingSourceFileCheckbox.addEventListener("change", () => {
                this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, fileUploadArea);
            });
            this.setFileUploadDisplayState(!useExistingSourceFileCheckbox.checked, fileUploadArea);
            return;
        }

        // If a source file is not in DataHub,
        // only allow uploading a new file.
        sourceFileOptionsFieldset.remove();
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