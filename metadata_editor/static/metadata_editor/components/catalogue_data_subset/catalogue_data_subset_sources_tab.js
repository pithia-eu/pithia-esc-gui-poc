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

    resetFieldErrorList(errorListElement) {
        errorListElement.replaceChildren();
    }

    addErrorToFieldErrorList(errorText, errorList) {
        const liElement = document.createElement("LI");
        liElement.className = "form-text text-danger";
        liElement.textContent = errorText;
        errorList.append(liElement);
    }

    addLoadingTextToFieldErrorList(loadingText, errorList) {
        const liElement = document.createElement("LI");
        liElement.className = "form-text";
        liElement.textContent = loadingText;
        errorList.append(liElement);
    }

    resetSourceNameErrors() {
        const sourceNameInputs = this.tabContent.querySelectorAll("input[name='source_name']");
        sourceNameInputs.forEach(input => input.classList.remove("is-invalid"));
        const errorLists = this.tabContent.querySelectorAll(".source-name-wrapper .field-error-list");
        for (const errorList of errorLists) {
            this.resetFieldErrorList(errorList);
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
                const closestErrorList = input.closest("div").querySelector("ul.field-error-list");
                this.addErrorToFieldErrorList(
                    errorText,
                    closestErrorList
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
        const closestErrorList = linkageInput.closest("div").querySelector("ul.field-error-list");
        linkageInput.classList.remove("is-invalid");
        this.resetFieldErrorList(closestErrorList);
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
        this.resetFieldErrorList(closestErrorList);
        this.addErrorToFieldErrorList(
            error,
            closestErrorList
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
        const linkageInput = newTabPane.querySelector("input[name='source_linkage']");
        const closestErrorList = linkageInput.closest("div").querySelector("ul.field-error-list");
        let linkageInputTimeout;
        this.checkLinkageUrlIsValidAndDisplayErrors(linkageInput);
        linkageInput.addEventListener("input", () => {
            if (linkageInputTimeout) {
                window.clearTimeout(linkageInputTimeout);
            }
            linkageInputTimeout = window.setTimeout(() => {
                this.checkLinkageUrlIsValidAndDisplayErrors(linkageInput);
            }, 500);
            this.resetFieldErrorList(closestErrorList);
            this.addLoadingTextToFieldErrorList("Checking link...", closestErrorList);
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

export function setupCatalogueDataSubsetSourcesTab() {
    const sourcesTab = new CatalogueDataSubsetSourcesTab();
    sourcesTab.setup();
    return sourcesTab;
}