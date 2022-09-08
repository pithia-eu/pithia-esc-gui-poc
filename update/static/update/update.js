import {
    handleFileUpload
} from "/static/register/register.js";

const fileInput = document.getElementById("id_file");
const fileValidationStatusElem = document.querySelector(".file-validation-status-container");

fileInput.addEventListener("change", async event => {
    await handleFileUpload(fileInput, fileValidationStatusElem, false, true);
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await handleFileUpload(fileInput, fileValidationStatusElem, false, true);
    }
});