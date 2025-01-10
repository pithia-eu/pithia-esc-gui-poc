import {
    setupOnlineResourceListAndLoadFiles,
} from "/static/register/catalogue_data_subset_form.js";
import {
    CatalogueDataSubsetOnlineResourceUpdateList,
} from "/static/update/catalogue_data_subset_source_updates.js";
const fileUploadForm = document.querySelector("#file-upload-form");


function exportDataHubFileUsage() {
    const dataHubFileCheckboxes = document.querySelectorAll("input[name='is_existing_datahub_file_used']");
    const dataHubFileUsage = {};
    for (const checkbox of dataHubFileCheckboxes) {
        dataHubFileUsage[checkbox.dataset.onlineResourceName] = checkbox.checked;
    }
    const onlineResourceDataHubFileUsageElement = document.querySelector("input[name='online_resource_datahub_file_usage']");
    onlineResourceDataHubFileUsageElement.value = JSON.stringify(dataHubFileUsage);
}

fileUploadForm.addEventListener("submit", e => {
    e.preventDefault();
    exportDataHubFileUsage();
    fileUploadForm.submit();
});

window.addEventListener("load", async () => {
    const onlineResourceList = new CatalogueDataSubsetOnlineResourceUpdateList();
    setupOnlineResourceListAndLoadFiles(onlineResourceList);
});