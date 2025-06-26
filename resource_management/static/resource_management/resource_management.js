import {
    setupDialog,
} from "/static/utils/dialogs.js";


const outdatedRegistrationsDialogShowButtons = document.querySelectorAll(".btn-show-outdated-regs-dialog");
const outdatedRegistrationsDialog = document.querySelector("#outdated-registrations-dialog");


// Outdated registrations check
async function checkAndLoadOutdatedRegistrationsList() {
    const outdatedRegistrationsCheckUrl = JSON.parse(document.querySelector("#outdated-resource-check-url-name").textContent);
    outdatedRegistrationsDialogShowButtons.forEach(button => {
        button.innerHTML = `
        <span class="spinner-grow spinner-grow-sm text-body-tertiary mt-1" role="status">
            <span class="visually-hidden">Loading...</span>
        </span> Checking for outdated registrations`;
    });
    const response = await fetch(outdatedRegistrationsCheckUrl);
    if (!response.ok) {
        const pElement = document.createElement("P");
        pElement.textContent = "Could not load data due to an error.";
        pElement.classList.add("mb-0");
        outdatedRegistrationsDialog.querySelector(".dialog-body").appendChild(pElement);
    }
    const responseText = await response.text();
    outdatedRegistrationsDialog.querySelector(".dialog-body").innerHTML = responseText;
    const numberOfOutdatedRegistrations = outdatedRegistrationsDialog.querySelectorAll(".dialog-body details").length;
    outdatedRegistrationsDialog.querySelector(".dialog-header span.text-secondary").textContent = `(${numberOfOutdatedRegistrations})`;
    outdatedRegistrationsDialogShowButtons.forEach(button => {
        button.removeAttribute("disabled");
        button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="fs-sm-1 bi bi-exclamation-circle-fill" style="transform: translateY(0.25rem);" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4m.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>
        </svg>${numberOfOutdatedRegistrations} outdated ${numberOfOutdatedRegistrations === 1 ? 'registration' : 'registrations'}`;
    });
}

// Event listeners
window.addEventListener("load", async () => {
    // Tooltip setup
    const bsTooltips = document.querySelectorAll("[data-bs-toggle='tooltip']");
    bsTooltips.forEach(elem => {
        new bootstrap.Tooltip(elem, {});
    });

    // Dialog setup
    const outdatedRegistrationsDialogCloseButton = document.querySelector("#outdated-registrations-dialog .btn-close");
    setupDialog(
        outdatedRegistrationsDialog,
        outdatedRegistrationsDialogShowButtons,
        outdatedRegistrationsDialogCloseButton
    );

    // Load outdated registrations list
    await checkAndLoadOutdatedRegistrationsList();
});