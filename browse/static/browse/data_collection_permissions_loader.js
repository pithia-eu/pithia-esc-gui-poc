const ONTOLOGY_NODE_PROPERTIES_MAPPING_URL = JSON.parse(document.getElementById("ontology-node-properties-mapping-url").textContent);


function getOntologyUrls() {
    const ontologyUrlElements = Array.from(document.querySelectorAll(".permission-ontology-server-url"));
    return ontologyUrlElements.map(el => el.dataset.metadataServerUrl);
}

async function getPropertiesForOntologyUrls(urls) {
    try {
        const formData = new FormData();
        formData.append('urls', JSON.stringify(urls));
        formData.append('properties', JSON.stringify([
            "definition",
        ]));
        formData.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
        const response = await fetch(ONTOLOGY_NODE_PROPERTIES_MAPPING_URL, {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        return json;
    } catch (error) {
        console.error(error);
    }
    return {};
}

function addPropertiesForOntologyUrlToPage(url, properties) {
    const ontologyDefinition = properties.skos_properties.definition;
    const ontologyDefinitionElements = document.querySelectorAll(`[data-metadata-server-url="${url}"] .permission-definition`);
    for (const el of ontologyDefinitionElements) {
        el.innerHTML = "";
        el.innerText = ontologyDefinition;
    }
}

function addPropertiesForOntologyUrlsToPage(propertiesByUrl) {
    for (const url in propertiesByUrl) {
        addPropertiesForOntologyUrlToPage(url, propertiesByUrl[url]);
    }
}

window.addEventListener("load", async() => {
    const urls = getOntologyUrls();
    const propertiesByUrl = await getPropertiesForOntologyUrls(urls);
    addPropertiesForOntologyUrlsToPage(propertiesByUrl);
});