function setupDialog(dialog, showButton, closeButton) {
    // Light dismiss - allows dialog to be closed
    // by clicking on the backdrop.
    dialog.addEventListener("click", () => {
        dialog.close();
    });

    dialog.querySelector(".dialog-content").addEventListener("click", event => {
        event.stopPropagation();
    });


    closeButton.addEventListener("click", () => {
        dialog.close();
    });

    dialog.addEventListener("close", () => {
        // When the dialog is closed, set the
        // inert attribute to true so that it's
        // not focusable by keyboard/assistive
        // technologies.
        dialog.setAttribute("inert", "");
    });

    showButton.addEventListener("click", () => {
        dialog.removeAttribute("inert");
        dialog.showModal();
        // Close button should autofocus with
        // dialog, but doesn't in Safari for
        // some reason.
        closeButton.focus();
    });
}

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

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

// Catalogues help dialog
const cataloguesHelpDialog = document.querySelector("#dialog-catalogues-help");
const cataloguesHelpDialogShowButton = document.querySelector("#btn-show-dialog-catalogues-help");
const cataloguesHelpDialogCloseButton = document.querySelector("#dialog-catalogues-help .btn-close");
setupDialog(cataloguesHelpDialog, cataloguesHelpDialogShowButton, cataloguesHelpDialogCloseButton);

// All scientific metadata help dialog
const allScientificMetadataHelpDialog = document.querySelector("#dialog-all-scientific-metadata-help");
const allScientificMetadataHelpDialogShowButton = document.querySelector("#btn-show-dialog-all-scientific-metadata-help");
const allScientificMetadataHelpDialogCloseButton = document.querySelector("#dialog-all-scientific-metadata-help .btn-close");
setupDialog(allScientificMetadataHelpDialog, allScientificMetadataHelpDialogShowButton, allScientificMetadataHelpDialogCloseButton);