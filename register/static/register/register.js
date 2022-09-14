import {
    handleFileUpload
} from "/static/file_upload.js";


const fileInput = document.getElementById("id_files");
const fileValidationStatusElem = document.querySelector(".file-validation-status-list");

fileInput.addEventListener("change", async event => {
    await handleFileUpload(fileInput, fileValidationStatusElem, true, false);
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await handleFileUpload(fileInput, fileValidationStatusElem, true, false);
    }
});