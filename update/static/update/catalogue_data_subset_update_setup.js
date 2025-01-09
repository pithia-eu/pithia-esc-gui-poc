import {
    setupOnlineResourceListAndLoadFiles,
} from "/static/register/catalogue_data_subset_form.js";
import {
    CatalogueDataSubsetOnlineResourceUpdateList,
} from "/static/update/catalogue_data_subset_source_updates.js";


window.addEventListener("load", async () => {
    const onlineResourceList = new CatalogueDataSubsetOnlineResourceUpdateList();
    const onlineResourceFileInputSwitch = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
    onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);
    setupOnlineResourceListAndLoadFiles(onlineResourceList);
});