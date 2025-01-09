import {
    CatalogueDataSubsetOnlineResourceList,
} from "/static/register/catalogue_data_subset_sources.js";
const namesOfOnlineResourcesWithDataHubFiles = JSON.parse(document.querySelector("#names-of-online-resources-with-files").textContent);


export class CatalogueDataSubsetOnlineResourceUpdateList extends CatalogueDataSubsetOnlineResourceList {
    updateDataHubCheckboxForOnlineResource(existingDataHubFileCheckbox, onlineResourceName) {
        existingDataHubFileCheckbox.name = existingDataHubFileCheckbox.name + "__" + onlineResourceName;
    }

    createListItem(onlineResource) {
        const onlineResourceFileListItem = super.createListItem(onlineResource);
        const existingDataHubFileCheckboxWrapper = onlineResourceFileListItem.querySelector(".existing-datahub-file-checkbox-wrapper");
        const onlineResourceName = onlineResource.querySelector("name").textContent;
        if (!namesOfOnlineResourcesWithDataHubFiles.includes(onlineResourceName)) {
            existingDataHubFileCheckboxWrapper.remove();
            return onlineResourceFileListItem;
        }
        const fileInputWrapper = onlineResourceFileListItem.querySelector(".file-input-wrapper");
        const fileInput = onlineResourceFileListItem.querySelector("input[type='file']");
        const labelForFileInput = onlineResourceFileListItem.querySelector(`label[for='${fileInput.id}']`);
        fileInputWrapper.classList.add("d-none");
        fileInput.removeAttribute("required");
        labelForFileInput.classList.remove("required");
        return onlineResourceFileListItem;
    }

    setupListItem(onlineResourceFileListItem, onlineResource) {
        super.setupListItem(onlineResourceFileListItem);
        // DataHub checkbox setup
        const onlineResourceName = onlineResource.querySelector("name").textContent;
        const existingDataHubFileCheckboxWrapper = onlineResourceFileListItem.querySelector(".existing-datahub-file-checkbox-wrapper");
        if (!existingDataHubFileCheckboxWrapper) {
            return;
        }
        const existingDataHubFileCheckbox = existingDataHubFileCheckboxWrapper.querySelector("input[type='checkbox']");
        this.updateDataHubCheckboxForOnlineResource(existingDataHubFileCheckbox, onlineResourceName);
        existingDataHubFileCheckbox.addEventListener("change", () => {
            const fileInputWrapper = onlineResourceFileListItem.querySelector(".file-input-wrapper");
            const fileInput = onlineResourceFileListItem.querySelector("input[type='file']");
            const labelForFileInput = onlineResourceFileListItem.querySelector(`label[for='${fileInput.id}']`);
            if (existingDataHubFileCheckbox.checked) {
                fileInputWrapper.classList.add("d-none");
                fileInput.removeAttribute("required");
                return labelForFileInput.classList.remove("required");
            }
            fileInputWrapper.classList.remove("d-none");
            fileInput.setAttribute("required", "true");
            return labelForFileInput.classList.add("required");
        });
    }
}