import {
    generateUniqueElemIdFromCurrentElemId,
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/metadata_editor/components/utils.js";


export class DynamicEditorTab {
    constructor(tabListSelector, tabContentSelector, tabPaneContentTemplateSelector, removeTabAndTabPaneButtonSelector, jsonExportElementSelector, tabButtonPrefixText = "Tab") {
        this.tabList = document.querySelector(tabListSelector);
        this.tabContent = document.querySelector(tabContentSelector);
        this.tabPaneContentTemplate = JSON.parse(document.querySelector(tabPaneContentTemplateSelector).textContent);
        this.removeTabAndTabPaneButtonSelector = removeTabAndTabPaneButtonSelector;
        this.jsonExportElement = document.querySelector(jsonExportElementSelector);
        this.tabButtonPrefixText = tabButtonPrefixText;
        this.createTabElement = this.tabList.querySelector(".create-tab");
        this.createTabButton = this.tabList.querySelector(".create-tab button");
        this.nextTabNumber = 2;
        this.numNewTabs = 0;
        this.deletedTabIndexSequence = [];
    }

    // Initial setup
    setup() {
        const firstTabPane = this.tabContent.querySelector(".tab-pane");
        this.loadPreviousTabData();
        this.setupTabPaneEventListeners(firstTabPane);
        this.createTabButton.addEventListener("click", () => {
            const newTabPane = this.createTabAndTabPane();
            this.createTabOnClickActions(newTabPane);
            this.exportTabData();
        });
    }

    // Utils
    getParentTabPaneOfChildNode(childNode) {
        const tabPanes = this.tabContent.querySelectorAll(".tab-pane");
        for (const tabPane of tabPanes) {
            if (tabPane.contains(childNode)) {
                return tabPane;
            }
        }
    }

    getTabButtonOfTabPane(tabPane) {
        const tabPaneLabelledBy = tabPane.getAttribute("aria-labelledby");
        const correspondingTabButton = document.getElementById(tabPaneLabelledBy);
        return correspondingTabButton;
    }

    // Helpers
    disableFirstRemoveTabAndTabPaneButtonIfOnlyOneTab() {
        const firstRemoveTabAndTabPaneButton = this.tabContent.querySelector(this.removeTabAndTabPaneButtonSelector);
        firstRemoveTabAndTabPaneButton.disabled = this.tabContent.querySelectorAll(".tab-pane").length === 1;
    }

    focusLastTabPane() {
        const tabs = this.tabList.querySelectorAll("button[aria-controls]");
        const lastTab = tabs[tabs.length - 1];
        lastTab.click();
    }

    switchToTabPaneContainingChildNode(childNode) {
        const containingTabPane = this.getParentTabPaneOfChildNode(childNode);
        const correspondingTabButton = this.getTabButtonOfTabPane(containingTabPane);
        correspondingTabButton.click();
    }

    getTabPaneIndex(tabPane) {
        return Array.from(this.tabContent.children).indexOf(tabPane);
    }

    // Tab removal
    removeTabAndTabPane(childNode) {
        const containingTabPane = this.getParentTabPaneOfChildNode(childNode);
        const correspondingTabButton = this.getTabButtonOfTabPane(containingTabPane)
        const containingTabListItem = correspondingTabButton.parentElement;
        const containingTabPaneIndex = this.getTabPaneIndex(containingTabPane);
        this.tabContent.removeChild(containingTabPane);
        this.tabList.removeChild(containingTabListItem);
        this.disableFirstRemoveTabAndTabPaneButtonIfOnlyOneTab();
        return containingTabPaneIndex;
    }

    // Tab setup
    setupRemoveTabAndTabPaneButton(removeTabAndTabPaneButton) {
        removeTabAndTabPaneButton.addEventListener("click", e => {
            const deletedTabPaneIndex = this.removeTabAndTabPane(e.currentTarget);
            this.addTabToDeletedTabSequence(deletedTabPaneIndex);
            this.exportTabData();
            this.focusLastTabPane();
        });
    }

    setupInvalidInputEventListeners(inputs, selects) {
        inputs.forEach(input => {
            input.addEventListener("invalid", e => {
                this.switchToTabPaneContainingChildNode(e.currentTarget);
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("invalid", e => {
                this.switchToTabPaneContainingChildNode(e.currentTarget);
            });
        });
    }

    setupTabPaneEventListeners(tabPane) {
        this.setupInvalidInputEventListeners(
            Array.from(tabPane.querySelectorAll("input")),
            Array.from(tabPane.querySelectorAll("select"))
        );

        const tables = tabPane.querySelectorAll("table");

        tables.forEach(table => {
            table.addEventListener("newTableRowInputsAdded", e => {
                const inputsSelector = (e.detail.inputIds).map(id => `#${id}`).join(", ")
                const selectsSelector = (e.detail.selectIds).map(id => `#${id}`).join(", ")
                this.setupInvalidInputEventListeners(
                    (inputsSelector) ? Array.from(tabPane.querySelectorAll(inputsSelector)) : [],
                    (selectsSelector) ? Array.from(tabPane.querySelectorAll(selectsSelector)) : []
                );
            });
        });
    
        const removeTabAndTabPaneButton = tabPane.querySelector(this.removeTabAndTabPaneButtonSelector);
        this.setupRemoveTabAndTabPaneButton(removeTabAndTabPaneButton);
    }

    createTabAndTabPane() {
        // New tab
        const newTab = document.createElement("LI");
        newTab.className = "nav-item";
        newTab.setAttribute("role", "presentation");
        
        // New tab button
        const newTabButton = document.createElement("BUTTON");
        const newTabIdPrefix = generateUniqueElemIdFromCurrentElemId(this.tabButtonPrefixText.toLowerCase().replace(/\s/g, ""));
        newTabButton.className = "nav-link";
        newTabButton.id = `${newTabIdPrefix}-tab`;
        newTabButton.dataset.bsToggle = "tab";
        newTabButton.dataset.bsTarget = `#${newTabIdPrefix}-tab-pane`;
        newTabButton.type = "button";
        newTabButton.role = "tab";
        newTabButton.setAttribute("aria-controls", `${newTabIdPrefix}-tab-pane`);
        newTabButton.textContent = `${this.tabButtonPrefixText} ${this.nextTabNumber}`;
    
        // Add new tab button to tab
        newTab.appendChild(newTabButton);
    
        // Append to current list
        this.tabList.insertBefore(newTab, this.createTabElement);
    
        // Create corresponding tab pane
        const newTabPane = this.createTabPane(newTabIdPrefix);
        this.setupTabPaneEventListeners(newTabPane);
        
        // Show the newly created tab
        this.focusLastTabPane();
    
        this.nextTabNumber += 1;

        return newTabPane;
    }

    createTabPane(newTabIdPrefix) {
        // Attributes
        const newTabPane = document.createElement("DIV");
        newTabPane.className = "tab-pane fade";
        newTabPane.id = `${newTabIdPrefix}-tab-pane`;
        newTabPane.setAttribute("role", "tabpanel");
        newTabPane.setAttribute("aria-labelledby", `${newTabIdPrefix}-tab`);
        newTabPane.setAttribute("tabindex", "0");
    
        // Content
        newTabPane.innerHTML = this.tabPaneContentTemplate;
        const elemsWithIds = newTabPane.querySelectorAll("[id]");
        updateDuplicatedElemsWithIdsInContainer(elemsWithIds, newTabPane);
    
        // Enable remove tab and tab pane button
        const removeTabAndTabPaneButton = newTabPane.querySelector(this.removeTabAndTabPaneButtonSelector);
        // removeTabAndTabPaneButton.querySelector(".remove-tab-pane-button-text").textContent = `Remove ${this.tabButtonPrefixText} ${this.nextTabNumber}`;
        removeTabAndTabPaneButton.disabled = false;
    
        this.tabContent.appendChild(newTabPane);
    
        this.disableFirstRemoveTabAndTabPaneButtonIfOnlyOneTab();
    
        const tabPaneControls = Array.from(newTabPane.querySelectorAll("input, textarea, select"));
        const selects = Array.from(newTabPane.querySelectorAll("select:not([multiple])"));
        const multipleChoiceSelects = Array.from(newTabPane.querySelectorAll("select[multiple]"));

        if (tabPaneControls.length > 0) {
            tabPaneControls.forEach(control => {
                control.value = "";
            });
        }
        if (selects.length > 0) {
            window.dispatchEvent(new CustomEvent("newSelectsAdded", {
                detail: selects.map(select => select.id),
            }));
        }
        if (multipleChoiceSelects.length > 0) {
            window.dispatchEvent(new CustomEvent("newMultipleChoiceSelectsAdded", {
                detail: multipleChoiceSelects.map(select => select.id),
            }));
        }
    
        return newTabPane;
    }

    createTabOnClickActions(newTabPane) {
        this.incrementNumberOfNewTabs();
    }

    // Tab data saving/loading
    getTabDataAsJson() {
        // Implemented in child class
    }

    incrementNumberOfNewTabs() {
        this.numNewTabs += 1;
    }

    addTabToDeletedTabSequence(tabIndex) {
        this.deletedTabIndexSequence.push(tabIndex);
    }

    exportTabData() {
        this.jsonExportElement.value = JSON.stringify(this.getTabDataAsJson());
        window.dispatchEvent(new CustomEvent("dynamicTabDataExported"));
    }

    loadPreviousTabData() {
    }
}