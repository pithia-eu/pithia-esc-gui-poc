import {
    setupOnlineResourceListAndLoadFiles,
} from "/static/register/data_subset_form.js";
import {
    DataSubsetOnlineResourceList,
} from "/static/register/data_subset_sources.js";


window.addEventListener("load", async () => {
    const onlineResourceList = new DataSubsetOnlineResourceList();
    setupOnlineResourceListAndLoadFiles(onlineResourceList);
});