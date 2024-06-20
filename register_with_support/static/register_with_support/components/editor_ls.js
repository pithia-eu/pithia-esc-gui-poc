import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

let wizardData = {};

function getAllWizardFields() {
    return editorForm.querySelectorAll("input[id], select[id], textarea[id");
}

function setupWizardFieldEventListeners() {
    const fields = getAllWizardFields();

    fields.forEach(field => {
        field.addEventListener("input", () => {
            saveWizardDataToLocalStorage();
        });
    });
}

function saveWizardDataToLocalStorage() {
    const wizardDataCopy = structuredClone(wizardData);
    try {
        const fields = getAllWizardFields();
        fields.forEach(field => {
            wizardDataCopy[field.id] = field.value;
        });
        wizardData = wizardDataCopy;
        window.localStorage.setItem("wizardData", JSON.stringify(wizardData));
        console.log("Wizard data saved:", wizardData);
    } catch (error) {
        console.log("Couldn't save wizard data due to an error.");
        console.error(error);
    }
}

function loadPastWizardData() {
    const pastWizardDataLS = window.localStorage.getItem("wizardData");
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

window.addEventListener("load", () => {
    setupWizardFieldEventListeners();
    loadPastWizardData();
    addWizardDataToForm(wizardData);
});