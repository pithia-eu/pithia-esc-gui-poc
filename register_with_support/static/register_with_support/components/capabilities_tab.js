import {
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/register_with_support/components/utils.js";

const capabilitiesTabList = document.querySelector("#capabilities-tab");
const capabilitiesTabContent = document.querySelector("#capabilities-tab-content");
const capabilitiesTabContentTemplate = JSON.parse(document.getElementById("capabilities-tab-content-template").textContent);
const createTabElement = document.querySelector(".create-tab");
const createTabButton = document.querySelector(".create-tab button");
let nextTabNumber = 2;


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
    createTabPane(nextTabNumber);

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
}

export function setupCapabilitiesTab() {
    createTabButton.addEventListener("click", () => {
        createTabAndTabPane();
    });
}