const metadataServerUrlBase = "https://metadata.pithia.eu";

function getServerUrlConversionUrl() {
    let serverUrlConversionUrl = JSON.parse(document.getElementById("server-url-conversion-url").textContent);
    const serverUrlAnchorTags = document.querySelectorAll(`a[href^="${metadataServerUrlBase}"]`);
    let ontologyServerUrls = [];
    let resourceServerUrls = [];
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
    if (ontologyServerUrls.length === 0 && resourceServerUrls.length === 0) {
        return serverUrlConversionUrl;
    }
    serverUrlConversionUrl += "?";
    if (ontologyServerUrls.length > 0) {
        ontologyServerUrls = ontologyServerUrls.map(url => encodeURIComponent(url));
        serverUrlConversionUrl += `ontology-server-urls=${ontologyServerUrls.join(",")}&`;
    }
    if (resourceServerUrls.length > 0) {
        resourceServerUrls = resourceServerUrls.map(url => encodeURIComponent(url));
        serverUrlConversionUrl += `resource-server-urls=${resourceServerUrls.join(",")}`;
    }
    return serverUrlConversionUrl;
}

function revealMetadataLink(tag, annotationText) {
    setTimeout(() => {
        tag.parentElement.querySelector(".placeholder-wrapper").style.display = "none";
        if (annotationText) {
            addAnnotationToMetadataLink(annotationText, tag.parentElement);
        }
        tag.style.display = "inline";
        tag.parentElement.classList.remove("updating");
        tag.parentElement.classList.remove("loading");
    }, 300);
    tag.parentElement.classList.add("updating");
}

function addAnnotationToMetadataLink(text, element) {
    const smallText = document.createElement("small");
    smallText.innerHTML = text;
    smallText.className = "text-muted";
    element.parentElement.append(smallText);
}

function convertOntologyServerUrlsAndResourceServerUrls() {
    const fetchParams = { method: "GET" };
    fetch(getServerUrlConversionUrl(), fetchParams)
        .then(response => response.json())
        .then(responseContent => {
            const convertedOntologyUrlMappings = responseContent.ontology_urls;
            const convertedResourceUrlMappings = responseContent.resource_urls;

            // Checking whether some URLs have not been converted
            // before actually making changes to links in the page.
            const originalOntologyUrls = responseContent.ontology_urls.map(urlMapping => urlMapping.original_server_url);
            const originalResourceUrls = responseContent.resource_urls.map(urlMapping => urlMapping.original_server_url);

            const metadataServerAnchorTags = document.querySelectorAll('span.metadata-server-url a');
            metadataServerAnchorTags.forEach(a => {
                if (!originalOntologyUrls.includes(a.href) && !originalResourceUrls.includes(a.href)) {
                    revealMetadataLink(a);
                }
            });

            convertedOntologyUrlMappings.forEach(urlMapping => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${urlMapping.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = urlMapping.converted_url;
                    tag.innerHTML = urlMapping.converted_url_text;
                    revealMetadataLink(tag, "(opens details of the ontology term in a new tab)");
                });
            });

            convertedResourceUrlMappings.forEach(urlMapping => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${urlMapping.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = urlMapping.converted_url;
                    tag.innerHTML = urlMapping.converted_url_text;
                    revealMetadataLink(tag, "(opens details of the metadata in a new tab)");
                });
            });
        })
        .catch (error => {
            console.error(`Could not get converted versions of metadata urls.`);
            console.error(error);
        });
}

window.onload = convertOntologyServerUrlsAndResourceServerUrls;