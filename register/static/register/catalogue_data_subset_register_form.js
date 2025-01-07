import {
    CatalogueDataSubsetOnlineResourceList,
} from "/static/register/catalogue_data_subset_sources.js";

const onlineResourceFileInputSwitch = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
const metadataFileInput = document.querySelector("input[name='files']");
let onlineResourceList;


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
        return onlineResourceList.reset();
    }
    const metadataFile = metadataFileInput.files[0];
    const xmlFileString = await metadataFile.text();
    onlineResourceList.load(xmlFileString);
}

onlineResourceFileInputSwitch.addEventListener("change", () => {
    onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);
});

metadataFileInput.addEventListener("change", async () => {
    await loadOnlineResourcesFromMetadataFile();
});

document.addEventListener("trackedFilesChanged", async () => {
    await loadOnlineResourcesFromMetadataFile();
});

window.addEventListener("load", async () => {
    setupFormSubmitButtonSpinner();
    onlineResourceList = new CatalogueDataSubsetOnlineResourceList();
    onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);
    await loadOnlineResourcesFromMetadataFile();
});