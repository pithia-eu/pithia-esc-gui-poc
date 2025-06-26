import {
    setupDialog,
} from "/static/utils/dialogs.js";

// Search by content help dialog
const searchByContentHelpDialog = document.querySelector("#dialog-search-by-content-help");
const searchByContentHelpDialogShowButtons = document.querySelectorAll("#btn-show-dialog-search-by-content-help");
const searchByContentHelpDialogCloseButton = document.querySelector("#dialog-search-by-content-help .btn-close");
setupDialog(
    searchByContentHelpDialog,
    searchByContentHelpDialogShowButtons,
    searchByContentHelpDialogCloseButton
);

// Simple search help dialog
const simpleSearchHelpDialog = document.querySelector("#dialog-simple-search-help");
const simpleSearchHelpDialogShowButtons = document.querySelectorAll("#btn-show-dialog-simple-search-help");
const simpleSearchHelpDialogCloseButton = document.querySelector("#dialog-simple-search-help .btn-close");
setupDialog(
    simpleSearchHelpDialog,
    simpleSearchHelpDialogShowButtons,
    simpleSearchHelpDialogCloseButton
);

// Data Collections help dialog
const dataCollectionsHelpDialog = document.querySelector("#dialog-data-collections-help");
const dataCollectionsHelpDialogShowButtons = document.querySelectorAll("#btn-show-dialog-data-collections-help");
const dataCollectionsHelpDialogCloseButton = document.querySelector("#dialog-data-collections-help .btn-close");
setupDialog(
    dataCollectionsHelpDialog,
    dataCollectionsHelpDialogShowButtons,
    dataCollectionsHelpDialogCloseButton
);

window.onload = () => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}