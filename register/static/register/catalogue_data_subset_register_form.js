import {
    clearOnlineResourceList,
    loadOnlineResourceFiles,
} from "/static/register/catalogue_data_subset_sources.js";

const metadataFileInput = document.querySelector("input[name='files']");


function setupFormSubmitButtonSpinner() {
    const form = document.querySelector("#file-upload-form");
    const formSubmitButton = form.querySelector("button[type='submit']");
    const originalFormSubmitButtonText = formSubmitButton.textContent;
    formSubmitButton.disabled = true;
    form.addEventListener("submit", () => {
        formSubmitButton.innerHTML = `
            <span class="d-inline-flex align-items-center column-gap-2">
                <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
                <span role="status">${originalFormSubmitButtonText}</span>
            </span>
        `;
        formSubmitButton.disabled = true;
    });
}

async function loadOnlineResourcesFromMetadataFile() {
    if (!metadataFileInput.files.length) {
        return clearOnlineResourceList();
    }
    const metadataFile = metadataFileInput.files[0];
    const xmlFileString = await metadataFile.text();
    loadOnlineResourceFiles(xmlFileString);
}

metadataFileInput.addEventListener("change", async () => {
    await loadOnlineResourcesFromMetadataFile();
});

document.addEventListener("trackedFilesChanged", async () => {
    await loadOnlineResourcesFromMetadataFile();
});

window.addEventListener("load", async () => {
    setupFormSubmitButtonSpinner();
    await loadOnlineResourcesFromMetadataFile();
});