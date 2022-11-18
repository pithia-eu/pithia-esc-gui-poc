const metadataServerUrlBase = "https://metadata.pithia.eu";

function convertOntologyServerUrlsAndResourceServerUrls() {
    const serverUrlConversionUrl = JSON.parse(document.getElementById("server-url-conversion-url").textContent);
    const serverUrlAnchorTags = document.querySelectorAll(`a[href^="${metadataServerUrlBase}"]`);
    const ontologyServerUrls = [];
    const resourceServerUrls = [];
    const unknownServerUrls = [];
    serverUrlAnchorTags.forEach(tag => {
        if (tag.href.startsWith(`${metadataServerUrlBase}/ontology/`)) {
            ontologyServerUrls.push(tag.href);
        } else if (tag.href.startsWith(`${metadataServerUrlBase}/resources/`)) {
            resourceServerUrls.push(tag.href);
        } else {
            unknownServerUrls.push(tag.href);
        }
    });
    
    const fetchParams = { method: "GET" };
    fetch(`${serverUrlConversionUrl}?ontology-server-urls=${ontologyServerUrls.join(",")}&resource-server-urls=${resourceServerUrls.join(",")}`, fetchParams)
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(responseContent => {
            const convertedOntologyUrls = responseContent.ontology_urls;
            const convertedResourceUrls = responseContent.resource_urls;

            convertedOntologyUrls.forEach(conversionDetails => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${conversionDetails.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = conversionDetails.converted_url;
                    tag.innerHTML = conversionDetails.converted_url_text;
                });
            });

            convertedResourceUrls.forEach(conversionDetails => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${conversionDetails.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = conversionDetails.converted_url;
                    tag.innerHTML = conversionDetails.converted_url_text;
                });
            });
        })
        .catch (error => {
            console.error(`Could not get converted versions of metadata urls.`);
            console.error(error);
        });
}

window.onload = convertOntologyServerUrlsAndResourceServerUrls;