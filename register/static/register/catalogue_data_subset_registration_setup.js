import {
    setupOnlineResourceListAndLoadFiles,
} from "/static/register/catalogue_data_subset_form.js";
import {
    CatalogueDataSubsetOnlineResourceList,
} from "/static/register/catalogue_data_subset_sources.js";


window.addEventListener("load", async () => {
    const onlineResourceList = new CatalogueDataSubsetOnlineResourceList();
    const onlineResourceFileInputSwitch = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");
    onlineResourceList.toggleVisibility(onlineResourceFileInputSwitch.checked);
    setupOnlineResourceListAndLoadFiles(onlineResourceList);
});