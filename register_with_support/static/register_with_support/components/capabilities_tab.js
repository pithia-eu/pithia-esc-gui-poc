import {
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/register_with_support/components/utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";

const capabilitiesTabList = document.querySelector("#capabilities-tab");
const capabilitiesTabContent = document.querySelector("#capabilities-tab-content");
const capabilitiesTabContentTemplate = JSON.parse(document.getElementById("capabilities-tab-content-template").textContent);
const createTabElement = document.querySelector(".create-tab");
const createTabButton = document.querySelector(".create-tab button");
let nextTabNumber = 2;


// Utils
function disableFirstRemoveCapabilityButtonIfOnlyOneTab() {
    const firstRemoveCapabilityButton = capabilitiesTabContent.querySelector(".remove-capability-button");
    firstRemoveCapabilityButton.disabled = capabilitiesTabContent.querySelectorAll(".tab-pane").length === 1;
}

function getContainingTabPane(childNode) {
    const tabPanes = capabilitiesTabContent.querySelectorAll(".tab-pane");
    for (const tabPane of tabPanes) {
        if (tabPane.contains(childNode)) {
            return tabPane;
        }
    }
}

function getCorrespondingTabButton(tabPane) {
    const tabPaneLabelledBy = tabPane.getAttribute("aria-labelledby");
    const correspondingTabButton = document.getElementById(tabPaneLabelledBy);
    return correspondingTabButton;
}

function focusLastTabPane() {
    const tabs = capabilitiesTabList.querySelectorAll("button[aria-controls]");
    const lastTab = tabs[tabs.length - 1];
    lastTab.click();
}

function updateTabPaneConditionalRequiredFieldStates(tabPane) {
    const requiredFields = tabPane.querySelectorAll("input[name='capability_name'], select[name='capability_observed_property']");
    const optionalFields = tabPane.querySelectorAll(`
        select[name='capability_dimensionality_instance'],
        select[name='capability_dimensionality_timeline'],
        input[name='capability_cadence'],
        select[name='capability_cadence_units'],
        select[name='capability_vector_representation'],
        select[name='capability_coordinate_system'],
        select[name='capability_units'],
        select[name='capability_qualifier']
    `);
    checkAndSetRequiredAttributesForFields(
        requiredFields,
        optionalFields
    );
}

function updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane) {
    const requiredFields = tabPane.querySelectorAll("input[name='capability_cadence'], select[name='capability_cadence_units']");
    checkAndSetRequiredAttributesForFields(
        requiredFields
    );
}

// Tab management
function removeCapability(childNode) {
    const containingTabPane = getContainingTabPane(childNode);
    const correspondingTabButton = getCorrespondingTabButton(containingTabPane)
    const containingTabListItem = correspondingTabButton.parentElement;
    capabilitiesTabContent.removeChild(containingTabPane);
    capabilitiesTabList.removeChild(containingTabListItem);
    disableFirstRemoveCapabilityButtonIfOnlyOneTab();
}

function setupRemoveCapabilityButton(removeCapabilityButton) {
    removeCapabilityButton.addEventListener("click", e => {
        removeCapability(e.currentTarget);
        saveCapabilitiesExportAsJSON();
        focusLastTabPane();
    });
}

function setupTabPaneFieldEventListeners(tabPane) {
    const inputs = tabPane.querySelectorAll("input");
    const selects = tabPane.querySelectorAll("select");

    inputs.forEach(input => {
        input.addEventListener("input", () => {
            saveCapabilitiesExportAsJSON();
            updateTabPaneConditionalRequiredFieldStates(tabPane);
            if (input.name === 'capability_cadence') {
                updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane);
            }
        });
        input.addEventListener("invalid", () => {
            const containingTabPane = getContainingTabPane(input);
            const correspondingTabButton = getCorrespondingTabButton(containingTabPane);
            correspondingTabButton.click();
        });
    });

    selects.forEach(select => {
        select.addEventListener("change", () => {
            saveCapabilitiesExportAsJSON();
            updateTabPaneConditionalRequiredFieldStates(tabPane);
            if (select.name === 'capability_cadence_units') {
                updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane);
            }
        });
        select.addEventListener("invalid", () => {
            const containingTabPane = getContainingTabPane(select);
            const correspondingTabButton = getCorrespondingTabButton(containingTabPane);
            correspondingTabButton.click();
        });
    });

    const removeCapabilityButton = tabPane.querySelector(".remove-capability-button");
    setupRemoveCapabilityButton(removeCapabilityButton);
}

function createTabAndTabPane() {
    // New tab
    const newTab = document.createElement("LI");
    newTab.className = "nav-item";
    newTab.setAttribute("role", "presentation");
    
    // New tab button
    const newTabButton = document.createElement("BUTTON");
    newTabButton.className = "nav-link";
    newTabButton.id = `c${nextTabNumber}-tab`;
    newTabButton.dataset.bsToggle = "tab";
    newTabButton.dataset.bsTarget = `#c${nextTabNumber}-tab-pane`;
    newTabButton.type = "button";
    newTabButton.role = "tab";
    newTabButton.setAttribute("aria-controls", `c${nextTabNumber}-tab-pane`);
    newTabButton.innerHTML = `Capability ${nextTabNumber}`;

    // Add new tab button to tab
    newTab.appendChild(newTabButton);

    // Append to current list
    capabilitiesTabList.insertBefore(newTab, createTabElement);

    // Create corresponding tab pane
    const newTabPane = createTabPane(nextTabNumber);
    setupTabPaneFieldEventListeners(newTabPane);
    
    // Show the newly created tab
    focusLastTabPane();

    nextTabNumber += 1;
}

function createTabPane(tabNumber) {
    // Attributes
    const newTabPane = document.createElement("DIV");
    newTabPane.className = "tab-pane fade";
    newTabPane.id = `c${tabNumber}-tab-pane`;
    newTabPane.setAttribute("role", "tabpanel");
    newTabPane.setAttribute("aria-labelledby", `c${tabNumber}-tab`);
    newTabPane.setAttribute("tabindex", "0");

    // Content
    newTabPane.innerHTML = capabilitiesTabContentTemplate;
    const elemsWithIds = newTabPane.querySelectorAll("[id]");
    updateDuplicatedElemsWithIdsInContainer(elemsWithIds, newTabPane);

    // Enable remove capability button
    const removeCapabilityButton = newTabPane.querySelector(".remove-capability-button");
    removeCapabilityButton.disabled = false;

    capabilitiesTabContent.appendChild(newTabPane);

    disableFirstRemoveCapabilityButtonIfOnlyOneTab();

    window.dispatchEvent(new CustomEvent("newSelectsAdded", {
        detail: Array.from(newTabPane.querySelectorAll("select:not([multiple])")).map(select => select.id),
    }));
    window.dispatchEvent(new CustomEvent("newMultipleChoiceSelectsAdded", {
        detail: Array.from(newTabPane.querySelectorAll("select[multiple]")).map(select => select.id),
    }));

    return newTabPane;
}

function exportCapabilities() {
    const capabilities = [];
    const capabilityTabPanes = capabilitiesTabContent.querySelectorAll(".tab-pane");
    capabilityTabPanes.forEach(tabPane => {
        const vectorRepresentationSelect = tabPane.querySelector("select[name='capability_vector_representation']");
        const vectorRepresentationSelectedOptions = Array.from(vectorRepresentationSelect.selectedOptions);
        const qualifierSelect = tabPane.querySelector("select[name='capability_qualifier']");
        const qualifierSelectedOptions = Array.from(qualifierSelect.selectedOptions);
        capabilities.push({
            name: tabPane.querySelector("input[name='capability_name']").value,
            observedProperty: tabPane.querySelector("select[name='capability_observed_property']").value,
            dimensionalityInstance: tabPane.querySelector("select[name='capability_dimensionality_instance']").value,
            dimensionalityTimeline: tabPane.querySelector("select[name='capability_dimensionality_timeline']").value,
            cadence: tabPane.querySelector("input[name='capability_cadence']").value,
            cadenceUnits: tabPane.querySelector("select[name='capability_cadence_units']").value,
            vectorRepresentation: vectorRepresentationSelectedOptions.map(option => option.value),
            coordinateSystem: tabPane.querySelector("select[name='capability_coordinate_system']").value,
            units: tabPane.querySelector("select[name='capability_units']").value,
            qualifier: qualifierSelectedOptions.map(option => option.value),
        });
    });
    return capabilities;
}

function saveCapabilitiesExportAsJSON() {
    const capabilitiesExport = exportCapabilities();
    const capabilitiesJsonElement = document.querySelector("input[name='capabilities_json']");
    capabilitiesJsonElement.value = JSON.stringify(capabilitiesExport);
}

function loadPreviousCapabilities() {
    const previousCapabilities = JSON.parse(document.querySelector("input[name='capabilities_json']").value);
    if (!previousCapabilities) {
        return;
    }
    previousCapabilities.forEach((capability, i) => {
        if (i !== 0) {
            createTabAndTabPane();
        }
        const correspondingTabPane = capabilitiesTabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
        const selects = correspondingTabPane.querySelectorAll("select");
        correspondingTabPane.querySelector("input[name='capability_name']").value = capability.name;
        correspondingTabPane.querySelector("select[name='capability_observed_property']").value = capability.observedProperty;
        correspondingTabPane.querySelector("select[name='capability_dimensionality_instance']").value = capability.dimensionalityInstance;
        correspondingTabPane.querySelector("select[name='capability_dimensionality_timeline']").value = capability.dimensionalityTimeline;
        correspondingTabPane.querySelector("input[name='capability_cadence']").value = capability.cadence;
        correspondingTabPane.querySelector("select[name='capability_cadence_units']").value = capability.cadenceUnits;
        correspondingTabPane.querySelector("select[name='capability_coordinate_system']").value = capability.coordinateSystem;
        correspondingTabPane.querySelector("select[name='capability_units']").value = capability.units;
        const vectorRepresentationSelect = correspondingTabPane.querySelector("select[name='capability_vector_representation']");
        vectorRepresentationSelect.value = "";
        capability.vectorRepresentation.forEach(component => {
            vectorRepresentationSelect.querySelector(`option[value="${component}"]`).selected = true;
        });
        const qualifierSelect = correspondingTabPane.querySelector("select[name='capability_qualifier']");
        qualifierSelect.value = "";
        capability.qualifier.forEach(qualifier => {
            qualifierSelect.querySelector(`option[value="${qualifier}"]`).selected = true;
        });

        selects.forEach(select => {
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: select.id,
            }));
        });
    });
    disableFirstRemoveCapabilityButtonIfOnlyOneTab();
}

export function setupCapabilitiesTab() {
    const firstTabPane = capabilitiesTabContent.querySelector(".tab-pane");
    loadPreviousCapabilities();
    setupTabPaneFieldEventListeners(firstTabPane);
    updateTabPaneConditionalRequiredFieldStates(firstTabPane);
    updateTabPaneConditionalRequiredCadenceRelatedFieldStates(firstTabPane);

    createTabButton.addEventListener("click", () => {
        createTabAndTabPane();
        saveCapabilitiesExportAsJSON();
    });
}