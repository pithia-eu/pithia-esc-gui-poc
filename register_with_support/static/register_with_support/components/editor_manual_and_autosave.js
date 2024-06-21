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


function saveWizardDataToLocalStorage() {
    const wizardDataCopy = structuredClone(wizardData);
    try {
        const textFields = getWizardTextFields();
        textFields.forEach(textField => {
            wizardDataCopy[textField.id] = textField.value;
        });

        const choiceFields = getWizardChoiceFields();
        choiceFields.forEach(choiceField => {
            wizardDataCopy[choiceField.id] = Array.from(choiceField.selectedOptions).map(option => option.value);
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
        if (field.tagName.toLowerCase() === "select") {
            for (const value of pastWizardData[fieldId]) {
                const correspondingOption = field.querySelector(`option[value="${value}"]`);
                if (!correspondingOption) continue;
                correspondingOption.selected = true;
            }
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: field.id,
            }));
            continue;
        }
        field.value = pastWizardData[fieldId];
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
    addWizardDataToForm(wizardData);
}