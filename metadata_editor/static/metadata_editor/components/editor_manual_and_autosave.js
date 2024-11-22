import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";

const saveButtons = document.querySelectorAll(".btn-save-data");
const resetButtons = document.querySelectorAll(".btn-reset-wizard");
const localStorageItemKey = JSON.parse(document.getElementById("save-data-local-storage-key").textContent);
let wizardData = {};


// Dynamic table and tab fields are not taken into
// account as these are handled by the the dynamic
// table and tab modules.
function getAllWizardFields() {
    return editorForm.querySelectorAll(`
        input[id]:not(.table input, .tab-pane input, .ts-control input[role="combobox"]),
        select[id]:not(.table select, .tab-pane select),
        textarea[id]:not(.table textarea, .tab-pane textarea)
    `);
}

function getWizardTextFields() {
    return editorForm.querySelectorAll(`
        input[id]:not(.table input, .tab-pane input, .ts-control input[role="combobox"], input[type="radio"], input[type="file"]),
        textarea[id]:not(.table textarea, .tab-pane textarea)
    `);
}

function getWizardSelectFields() {
    return editorForm.querySelectorAll(`select[id]:not(.table select, .tab-pane select)`);
}

function getWizardCheckedRadioButtons() {
    return editorForm.querySelectorAll('input[id][type="radio"]:not(.table input[type="radio"], .tab-pane input[type="radio"]):checked');
}

function updateSaveStatus(status) {
    const savedStatusElements = document.querySelectorAll(".last-saved-at");
    savedStatusElements.forEach(elem => {
        elem.textContent = status;
    });
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
    updateSaveStatus(`Last saved in browser ${lastSavedFormatted}`);
}

// Credit: https://stackoverflow.com/a/20672625
function resetDialog(message, success, failure) {
    const openTime = new Date();
    const result = confirm(message);
    const closeTime = new Date();

    if (closeTime - openTime < 10) {
        return failure();
    } else {
        return success(result);
    }
}

function resetWizard() {
    editorForm.reset();
}

function resetWizardAndRemovePastWizardData() {
    resetWizard();
    removePastWizardData();
    window.location.reload();
}

function confirmResetWizard() {
    resetDialog(
        "All fields will be set to their initial values. Any existing save data will also be erased.",
        (result) => {
            if (!result) return;
            resetWizardAndRemovePastWizardData();
        }, resetWizardAndRemovePastWizardData);
}


function saveWizardDataToLocalStorage() {
    const wizardDataCopy = structuredClone(wizardData);
    wizardDataCopy.fieldData = {};
    try {
        const textFields = getWizardTextFields();
        textFields.forEach(textField => {
            wizardDataCopy.fieldData[textField.id] = textField.value;
        });

        const selectFields = getWizardSelectFields();
        selectFields.forEach(selectField => {
            wizardDataCopy.fieldData[selectField.id] = Array.from(selectField.selectedOptions).map(option => option.value);
        });

        wizardDataCopy.checkedRadioButtonIds = Array.from(getWizardCheckedRadioButtons()).map(checkedRadioButton => checkedRadioButton.id);
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

function removePastWizardData() {
    if (!localStorageItemKey) return;
    const pastWizardDataLS = window.localStorage.getItem(localStorageItemKey);
    if (!pastWizardDataLS) {
        console.log("No past wizard data found.");
        return;
    }
    window.localStorage.removeItem(localStorageItemKey);
}

function addFieldDataToForm(fieldData) {
    for (const fieldId in fieldData) {
        try {
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
        } catch (error) {
            console.error(error);
        }
    }
}

function addRadioButtonDataToForm(checkedRadioButtonIds) {
    for (const radioButtonId of checkedRadioButtonIds) {
        const radioButton = editorForm.querySelector(`#${radioButtonId}`);
        if (!radioButton) continue;
        radioButton.checked = true;
    }
}

function setupResetButtonEventListeners() {
    resetButtons.forEach(resetButton => {
        resetButton.addEventListener("click", () => {
            confirmResetWizard();
        });
    });
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

    saveButtons.forEach(saveButton => {
        saveButton.addEventListener("click", () => {
            saveWizardDataToLocalStorage();
        });
    });

    setupResetButtonEventListeners();
}

export function setupWizardManualAndAutoSave() {
    if (!localStorageItemKey || localStorageItemKey.length === 0) {
        const msg = "Saving is currently unavailable. Changes will not be saved.";
        saveButtons.forEach(saveButton => {
            saveButton.disabled = true;
            saveButton.classList.add("disabled");
        });
        setupResetButtonEventListeners();
        return updateSaveStatus(msg);
    }
    const urlParams = new URLSearchParams(window.location.search);
    const isPastWizardDataReset = urlParams.get("reset");
    if (isPastWizardDataReset) removePastWizardData();
    setupEventListeners();
    loadPastWizardData();
    addFieldDataToForm(wizardData.fieldData);
    if ('checkedRadioButtonIds' in wizardData) {
        addRadioButtonDataToForm(wizardData.checkedRadioButtonIds);
    }
}