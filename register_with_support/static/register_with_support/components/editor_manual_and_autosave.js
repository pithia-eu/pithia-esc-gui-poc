import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

let wizardData = {};
let localStorageItemKey;


function getAllWizardFields() {
    // Dynamic table and tab fields are not taken into
    // account as these are handled by the the dynamic
    // table and tab modules.
    return editorForm.querySelectorAll(`
        input[id]:not(.table input, .tab-pane input),
        select[id]:not(.table select, .tab-pane select),
        textarea[id]:not(.table textarea, .tab-pane textarea)
    `);
}

function saveWizardDataToLocalStorage() {
    const wizardDataCopy = structuredClone(wizardData);
    try {
        const fields = getAllWizardFields();
        fields.forEach(field => {
            wizardDataCopy[field.id] = field.value;
        });
        wizardData = wizardDataCopy;
        window.localStorage.setItem(localStorageItemKey, JSON.stringify(wizardData));
        console.log("Wizard data saved:", wizardData);
    } catch (error) {
        console.log("Couldn't save wizard data due to an error.");
        console.error(error);
    }
}

function loadPastWizardData() {
    const pastWizardDataLS = window.localStorage.getItem(localStorageItemKey);
    if (!pastWizardDataLS) return;
    console.log("Past wizard data found.");
    const pastWizardData = JSON.parse(pastWizardDataLS);

    try {
        wizardData = pastWizardData;
    } catch (error) {
        console.log("There was an error loading past wizard data.")
        console.error(error);
    }
}

function addWizardDataToForm(pastWizardData) {
    for (const fieldId in pastWizardData) {
        const field = editorForm.querySelector(`#${fieldId}`);
        if (!field) continue;
        field.value = pastWizardData[fieldId];
        if (field.tagName.toLowerCase() === "select") {
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: field.id,
            }));
        }
    }
}

function setupEventListeners() {
    const fields = getAllWizardFields();

    fields.forEach(field => {
        field.addEventListener("input", () => {
            saveWizardDataToLocalStorage();
        });
    });

    window.addEventListener("dynamicTableDataExported", () => {
        saveWizardDataToLocalStorage();
    });
    
    window.addEventListener("dynamicTabDataExported", () => {
        saveWizardDataToLocalStorage();
    });
}

export function setupWizardManualAndAutoSave(localStorageItemKeyForWizard) {
    // Changes depending on the wizard type
    localStorageItemKey = localStorageItemKeyForWizard;

    setupEventListeners();
    loadPastWizardData();
    addWizardDataToForm(wizardData);
}