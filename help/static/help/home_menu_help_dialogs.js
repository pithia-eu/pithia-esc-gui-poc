import {
    setupDialog,
} from "/static/help/help_dialogs.js";

// Search by content help dialog
const searchByContentHelpDialog = document.querySelector("#dialog-search-by-content-help");
const searchByContentHelpDialogShowButton = document.querySelector("#btn-show-dialog-search-by-content-help");
const searchByContentHelpDialogCloseButton = document.querySelector("#dialog-search-by-content-help .btn-close");
setupDialog(searchByContentHelpDialog, searchByContentHelpDialogShowButton, searchByContentHelpDialogCloseButton);

// Simple search help dialog
const simpleSearchHelpDialog = document.querySelector("#dialog-simple-search-help");
const simpleSearchHelpDialogShowButton = document.querySelector("#btn-show-dialog-simple-search-help");
const simpleSearchHelpDialogCloseButton = document.querySelector("#dialog-simple-search-help .btn-close");
setupDialog(simpleSearchHelpDialog, simpleSearchHelpDialogShowButton, simpleSearchHelpDialogCloseButton);

// Data Collections help dialog
const dataCollectionsHelpDialog = document.querySelector("#dialog-data-collections-help");
const dataCollectionsHelpDialogShowButton = document.querySelector("#btn-show-dialog-data-collections-help");
const dataCollectionsHelpDialogCloseButton = document.querySelector("#dialog-data-collections-help .btn-close");
setupDialog(dataCollectionsHelpDialog, dataCollectionsHelpDialogShowButton, dataCollectionsHelpDialogCloseButton);

window.onload = () => {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}