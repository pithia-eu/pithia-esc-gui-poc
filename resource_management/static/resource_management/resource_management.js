import {
    setupDialog,
} from "/static/utils/dialogs.js";


window.addEventListener("load", () => {
    // Tooltip setup
    const bsTooltips = document.querySelectorAll("[data-bs-toggle='tooltip']");
    bsTooltips.forEach(elem => {
        new bootstrap.Tooltip(elem, {});
    });

    // Dialog setup
    const outdatedRegistrationsDialog = document.querySelector("#outdated-registrations-dialog");
    const outdatedRegistrationsDialogShowButtons = document.querySelectorAll(".btn-show-outdated-regs-dialog");
    const outdatedRegistrationsDialogCloseButton = document.querySelector("#outdated-registrations-dialog .btn-close");
    setupDialog(
        outdatedRegistrationsDialog,
        outdatedRegistrationsDialogShowButtons,
        outdatedRegistrationsDialogCloseButton
    );
});