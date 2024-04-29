import {
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/register_with_support/components/utils.js";

const capabilitiesTabList = document.querySelector("#capabilities-tab");
const capabilitiesTabContent = document.querySelector("#capabilities-tab-content");
const capabilitiesTabContentTemplate = JSON.parse(document.getElementById("capabilities-tab-content-template").textContent);
const createTabElement = document.querySelector(".create-tab");
const createTabButton = document.querySelector(".create-tab button");
let nextTabNumber = 2;


function setupTabPaneFieldEventListeners(tabPane) {
    const inputs = tabPane.querySelectorAll("input");
    const selects = tabPane.querySelectorAll("select");

    inputs.forEach(input => {
        input.addEventListener("input", () => {
            saveCapabilitiesExportAsJSON();
        });
    });

    selects.forEach(select => {
        select.addEventListener("change", () => {
            saveCapabilitiesExportAsJSON();
        });
    });
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

    capabilitiesTabContent.appendChild(newTabPane);

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
        capabilities.push({
            name: tabPane.querySelector("input[name='capability_name']").value,
            observedProperty: tabPane.querySelector("select[name='capability_observed_property']").value,
            dimensionalityInstance: tabPane.querySelector("select[name='capability_dimensionality_instance']").value,
            dimensionalityTimeline: tabPane.querySelector("select[name='capability_dimensionality_timeline']").value,
            cadence: tabPane.querySelector("input[name='capability_cadence']").value,
            vectorRepresentation: tabPane.querySelector("input[name='capability_vector_representation']").value,
            coordinateSystem: tabPane.querySelector("select[name='capability_coordinate_system']").value,
            units: tabPane.querySelector("select[name='capability_units']").value,
            qualifier: tabPane.querySelector("select[name='capability_qualifier']").value,
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
        correspondingTabPane.querySelector("input[name='capability_vector_representation']").value = capability.vectorRepresentation;
        correspondingTabPane.querySelector("select[name='capability_coordinate_system']").value = capability.coordinateSystem;
        correspondingTabPane.querySelector("select[name='capability_units']").value = capability.units;
        correspondingTabPane.querySelector("select[name='capability_qualifier']").value = capability.qualifier;
        selects.forEach(select => {
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: select.id,
            }));
        });
    });
}

export function setupCapabilitiesTab() {
    const firstTabPane = capabilitiesTabContent.querySelector(".tab-pane");
    setupTabPaneFieldEventListeners(firstTabPane);
    loadPreviousCapabilities();

    createTabButton.addEventListener("click", () => {
        createTabAndTabPane();
        saveCapabilitiesExportAsJSON();
    });
}