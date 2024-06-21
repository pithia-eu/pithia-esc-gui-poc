import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

const localStorageItemKey = JSON.parse(document.getElementById("save-data-local-storage-key").textContent);
let wizardData = {};


// Dynamic table and tab fields are not taken into
// account as these are handled by the the dynamic
// table and tab modules.
function getAllWizardFields() {
    return editorForm.querySelectorAll(`
        input[id]:not(.table input, .tab-pane input),
        select[id]:not(.table select, .tab-pane select),
        textarea[id]:not(.table textarea, .tab-pane textarea)
    `);
}

function getWizardTextFields() {
    return editorForm.querySelectorAll(`
        input[id]:not(.table input, .tab-pane input),
        textarea[id]:not(.table textarea, .tab-pane textarea)
    `);
}

function getWizardChoiceFields() {
    return editorForm.querySelectorAll(`select[id]:not(.table select, .tab-pane select)`);
}

function updateLastSavedStatus(lastSaved) {
    const lastSavedDate = new Date(lastSaved);
    const locales = [];
    const options = {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    };
    let lastSavedFormatted = lastSavedDate.toLocaleTimeString(locales, options);
    if (new Date(Date.now()).toDateString() !== lastSavedDate.toDateString()) {
        delete options.second;
        lastSavedFormatted = lastSavedDate.toLocaleDateString(locales, options);
    }
    document.querySelector("#last-saved-at").textContent = `Last saved ${lastSavedFormatted}`;
}


function saveWizardDataToLocalStorage() {
    const wizardDataCopy = structuredClone(wizardData);
    wizardDataCopy.fieldData = {};
    try {
        const textFields = getWizardTextFields();
        textFields.forEach(textField => {
            wizardDataCopy.fieldData[textField.id] = textField.value;
        });

        const choiceFields = getWizardChoiceFields();
        choiceFields.forEach(choiceField => {
            wizardDataCopy.fieldData[choiceField.id] = Array.from(choiceField.selectedOptions).map(option => option.value);
        });
        wizardDataCopy.lastSaved = Date.now();

        wizardData = wizardDataCopy;
        window.localStorage.setItem(localStorageItemKey, JSON.stringify(wizardData));
        console.log("Wizard data saved:", wizardData);
        updateLastSavedStatus(wizardData.lastSaved);
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
        updateLastSavedStatus(wizardData.lastSaved);
    } catch (error) {
        console.log("There was an error loading past wizard data.")
        console.error(error);
    }
}

function addFieldDataToForm(fieldData) {
    for (const fieldId in fieldData) {
        const field = editorForm.querySelector(`#${fieldId}`);
        if (!field) continue;
        if (field.tagName.toLowerCase() === "select") {
            for (const value of fieldData[fieldId]) {
                const correspondingOption = field.querySelector(`option[value="${value}"]`);
                if (!correspondingOption) continue;
                correspondingOption.selected = true;
            }
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: field.id,
            }));
            continue;
        }
        field.value = fieldData[fieldId];
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
    
    window.addEventListener("wizardFieldProgrammaticallySet", () => {
        saveWizardDataToLocalStorage();
    });
}

export function setupWizardManualAndAutoSave() {
    setupEventListeners();
    loadPastWizardData();
    addFieldDataToForm(wizardData.fieldData);
}