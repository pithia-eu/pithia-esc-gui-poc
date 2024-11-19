import {
    startNewRegistrationValidationProcess,
} from "/static/validation/inline_registration_validation.js";


const fileInput = document.querySelector("#id_files");


fileInput.addEventListener("change", async event => {
    await startNewRegistrationValidationProcess();
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startNewRegistrationValidationProcess();
    }
});