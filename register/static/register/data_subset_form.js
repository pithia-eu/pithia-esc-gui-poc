const onlineResourceFileInputSwitch = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
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

async function loadOnlineResourcesFromMetadataFile(onlineResourceList) {
    if (!metadataFileInput.files.length) {
        return onlineResourceList.reset();
    }
    const metadataFile = metadataFileInput.files[0];
    const xmlFileString = await metadataFile.text();
    onlineResourceList.load(xmlFileString);
}

export async function setupOnlineResourceListAndLoadFiles(onlineResourceList) {
    await loadOnlineResourcesFromMetadataFile(onlineResourceList);
    onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);

    onlineResourceFileInputSwitch.addEventListener("change", () => {
        onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);
    });
    
    metadataFileInput.addEventListener("change", async () => {
        await loadOnlineResourcesFromMetadataFile(onlineResourceList);
    });
    
    document.addEventListener("trackedFilesChanged", async () => {
        await loadOnlineResourcesFromMetadataFile(onlineResourceList);
    });
}

window.addEventListener("load", async () => {
    setupFormSubmitButtonSpinner();
});