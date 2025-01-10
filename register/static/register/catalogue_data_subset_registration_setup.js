import {
    setupOnlineResourceListAndLoadFiles,
} from "/static/register/catalogue_data_subset_form.js";
import {
    CatalogueDataSubsetOnlineResourceList,
} from "/static/register/catalogue_data_subset_sources.js";


window.addEventListener("load", async () => {
    const onlineResourceList = new CatalogueDataSubsetOnlineResourceList();
    setupOnlineResourceListAndLoadFiles(onlineResourceList);
});