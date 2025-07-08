import {
    checkAndSetRequiredAttributesForFieldsBySelectors,
} from "/static/metadata_editor/components/conditional_required_fields.js";
import {
    SourcesTab,
} from "/static/metadata_editor/components/sources_tab.js";
import {
    checkIfEscUrl,
} from "/static/metadata_editor/components/url_format_checker.js";
import {
    checkForSimilarSourceNames,
} from "/static/validation/data_subset_validation.js";


export class DataSubsetSourcesTab extends SourcesTab {
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
                input.removeAttribute("disabled");
            }
            inputWrapper.classList.remove("d-none");
        }
    }

    disableSourceFileSharingMethodForTabPane(tabPane, inputWrapperSelector) {
        const inputWrappersInTab = tabPane.querySelectorAll(inputWrapperSelector);
        for (const inputWrapper of inputWrappersInTab) {
            const inputsInWrapper = inputWrapper.querySelectorAll("input");
            for (const input of inputsInWrapper) {
                input.setAttribute("disabled", "true");
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
        this.isUsingDataHub = false;
        this.enabledSourceFileSharingMethodInputSelector = this.sourceLinkageInputSelector;
        this.enabledSourceFileSharingMethodInputWrapperSelector = this.sourceLinkageInputWrapperSelector;
        this.disabledSourceFileSharingMethodInputSelector = this.sourceFileInputSelector;
        this.disabledSourceFileSharingMethodInputWrapperSelector = this.sourceFileInputWrapperSelector;
        this.applySourceFileSharingMethodChoiceToAllTabPanes();
    }
    
    setSourceFileSharingMethodToFileUpload() {
        this.isUsingDataHub = true;
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

    getInvalidFeedbackElementForInput(input) {
        return document.querySelector(`#invalid-feedback-${input.id}`);
    }

    resetFieldInvalidFeedback(invalidFeedbackElement) {
        invalidFeedbackElement.replaceChildren();
    }

    updateInvalidFeedbackForField(errorText, invalidFeedbackElement) {
        invalidFeedbackElement.textContent = errorText;
    }

    showLoadingTextForLinkageField(sourceLinkageInputWrapper) {
        return sourceLinkageInputWrapper.querySelector(".loading-text").classList.remove("d-none");
    }

    hideLoadingTextForLinkageField(sourceLinkageInputWrapper) {
        return sourceLinkageInputWrapper.querySelector(".loading-text").classList.add("d-none");
    }

    resetSourceNameErrors() {
        const sourceNameInputs = this.tabContent.querySelectorAll("input[name='source_name']");
        sourceNameInputs.forEach(input => input.classList.remove("is-invalid"));
        const invalidFeedbackElementsForInputs = Array.from(sourceNameInputs).map(input => this.getInvalidFeedbackElementForInput(input));
        for (const invalidFeedbackElement of invalidFeedbackElementsForInputs) {
            this.resetFieldInvalidFeedback(invalidFeedbackElement);
        }
    }

    checkSourceNamesAreUnique() {
        const sourceNameInputs = this.tabContent.querySelectorAll("input[name='source_name']");
        const sourceNames = Array.from(sourceNameInputs).map(sourceNameInput => sourceNameInput.value);
        const sourceNamesGroupedByNormalised = checkForSimilarSourceNames(sourceNames);
        
        for (const sourceName in sourceNamesGroupedByNormalised) {
            if (!sourceName) {
                continue;
            }
            const unnormalisedVersionsOfSourceNames = sourceNamesGroupedByNormalised[sourceName];
            if (unnormalisedVersionsOfSourceNames.length <= 1) {
                continue;
            }
            const inputs = Array.from(this.tabContent.querySelectorAll("input[name='source_name']")).filter(input => {
                return unnormalisedVersionsOfSourceNames.includes(input.value);
            });
            inputs.forEach(input => {
                const inputsWithSimilarNames = inputs.filter(inputWithSimilarName => input.id !== inputWithSimilarName.id);
                input.classList.add("is-invalid");
                const errorText = `"${input.value.trim()}" is too similar to the names of ${inputsWithSimilarNames.length} other online resource${inputsWithSimilarNames.length === 1 ? '' : 's'}. Please enter a different name.`;
                const inputInvalidFeedbackElement = this.getInvalidFeedbackElementForInput(input);
                this.updateInvalidFeedbackForField(
                    errorText,
                    inputInvalidFeedbackElement
                );
            });
        }
    }

    checkLinkageUrlIsValid(linkageUrl) {
        const linkageOrFileCheckbox = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
        const linkageOrFileCheckboxLabel = document.querySelector(`label[for="${linkageOrFileCheckbox.id}"]`);
        try {
            const isLinkageUrlInternal = checkIfEscUrl(linkageUrl);
            if (isLinkageUrlInternal) {
                return {
                    valid: false,
                    error: `Please use the file upload functionality (enabled by toggling the "${linkageOrFileCheckboxLabel.textContent.trim()}" switch) to add a file to this online resource.`,
                }
            }
        } catch (error) {
            console.error(error);
            return {
                valid: false,
                error: "Please enter a URL",
            };
        }
        return {
            valid: true,
        };
    }

    checkLinkageUrlIsValidAndDisplayErrors(linkageInput) {
        const linkageUrl = linkageInput.value;
        const linkageInputInvalidFeedbackElement = this.getInvalidFeedbackElementForInput(linkageInput);
        this.resetFieldInvalidFeedback(linkageInputInvalidFeedbackElement);
        linkageInput.classList.remove("is-invalid");
        if (!linkageUrl.trim()) {
            return;
        }
        const {
            valid,
            error
        } = this.checkLinkageUrlIsValid(linkageUrl);
        if (valid) {
            return;
        }
        linkageInput.classList.add("is-invalid");
        this.resetFieldInvalidFeedback(linkageInputInvalidFeedbackElement);
        this.updateInvalidFeedbackForField(
            error,
            linkageInputInvalidFeedbackElement
        );
    }

    setupSourceNameCheckForTabPane(newTabPane) {
        const currentSourceNameInput = newTabPane.querySelector("input[name='source_name']");
        currentSourceNameInput.addEventListener("input", () => {
            this.resetSourceNameErrors();
            this.checkSourceNamesAreUnique();
        });
    }

    setupLinkageCheckForTabPane(newTabPane) {
        const sourceLinkageInputWrapper = newTabPane.querySelector(this.sourceLinkageInputWrapperSelector);
        const linkageInput = newTabPane.querySelector("input[name='source_linkage']");
        this.checkLinkageUrlIsValidAndDisplayErrors(linkageInput);
        
        let linkageInputTimeout;
        linkageInput.addEventListener("input", () => {
            if (linkageInputTimeout) {
                window.clearTimeout(linkageInputTimeout);
            }
            linkageInputTimeout = window.setTimeout(() => {
                this.hideLoadingTextForLinkageField(sourceLinkageInputWrapper);
                this.checkLinkageUrlIsValidAndDisplayErrors(linkageInput);
            }, 500);
            this.showLoadingTextForLinkageField(sourceLinkageInputWrapper);
        });
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        this.setupSourceNameCheckForTabPane(tabPane);
        this.setupLinkageCheckForTabPane(tabPane);
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

    loadPreviousTabPaneData(source, correspondingTabPane) {
        super.loadPreviousTabPaneData(source, correspondingTabPane);
        this.updateTabPaneConditionalRequiredFieldStates(correspondingTabPane);
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
        this.checkSourceNamesAreUnique();
    }
}

export function setupDataSubsetSourcesTab() {
    const sourcesTab = new DataSubsetSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}