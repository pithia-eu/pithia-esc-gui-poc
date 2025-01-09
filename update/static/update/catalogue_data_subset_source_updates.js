import {
    CatalogueDataSubsetOnlineResourceList,
} from "/static/register/catalogue_data_subset_sources.js";
const namesOfOnlineResourcesWithDataHubFiles = JSON.parse(document.querySelector("#names-of-online-resources-with-files").textContent);


export class CatalogueDataSubsetOnlineResourceUpdateList extends CatalogueDataSubsetOnlineResourceList {
    createListItem(onlineResource) {
        const onlineResourceFileListItem = super.createListItem(onlineResource);
        const existingDataHubFileCheckboxWrapper = onlineResourceFileListItem.querySelector(".existing-datahub-file-checkbox-wrapper");
        const onlineResourceName = onlineResource.querySelector("name").textContent;
        if (!namesOfOnlineResourcesWithDataHubFiles.includes(onlineResourceName)) {
            existingDataHubFileCheckboxWrapper.remove("d-none");
        }
        return onlineResourceFileListItem;
    }
}