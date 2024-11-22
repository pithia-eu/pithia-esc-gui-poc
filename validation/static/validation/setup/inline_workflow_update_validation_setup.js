import {
    startWorkflowMetadataFileUpdateValidationProcess,
} from "/static/validation/inline_workflow_validation.js";


const fileInput = document.querySelector("#id_files");


fileInput.addEventListener("change", async event => {
    await startWorkflowMetadataFileUpdateValidationProcess();
});

window.addEventListener("load", async event => {
    if (fileInput.value !== "") {
        // In case files have been entered into the file input
        // and the user refreshes the page.
        await startWorkflowMetadataFileUpdateValidationProcess();
    }
});