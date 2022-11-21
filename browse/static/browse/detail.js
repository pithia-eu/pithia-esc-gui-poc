const metadataServerUrlBase = "https://metadata.pithia.eu";

function getServerUrlConversionUrl() {
    let serverUrlConversionUrl = JSON.parse(document.getElementById("server-url-conversion-url").textContent);
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
    if (ontologyServerUrls.length == 0 && resourceServerUrls.length == 0) {
        return serverUrlConversionUrl;
    }
    serverUrlConversionUrl += "?";
    if (ontologyServerUrls.length > 0) {
        serverUrlConversionUrl += `ontology-server-urls=${ontologyServerUrls.join(",")}&`;
    }
    if (resourceServerUrls.length > 0) {
        serverUrlConversionUrl += `resource-server-urls=${resourceServerUrls.join(",")}`;
    }
    return serverUrlConversionUrl;
}

function convertOntologyServerUrlsAndResourceServerUrls() {
    const fetchParams = { method: "GET" };
    fetch(getServerUrlConversionUrl(), fetchParams)
        .then(response => response.json())
        .then(responseContent => {
            const convertedOntologyUrls = responseContent.ontology_urls;
            const convertedResourceUrls = responseContent.resource_urls;

            convertedOntologyUrls.forEach(conversionDetails => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${conversionDetails.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = conversionDetails.converted_url;
                    tag.innerHTML = conversionDetails.converted_url_text;
                    setTimeout(() => {
                        tag.parentElement.querySelector(".placeholder-wrapper").style.display = "none";
                        tag.style.display = "inline";
                    }, 300);
                    setTimeout(() => {
                        tag.style.opacity = "1";
                    }, 350);
                    tag.parentElement.querySelector(".placeholder-wrapper").style.opacity = "0";
                });
            });

            convertedResourceUrls.forEach(conversionDetails => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${conversionDetails.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = conversionDetails.converted_url;
                    tag.innerHTML = conversionDetails.converted_url_text;
                    setTimeout(() => {
                        tag.parentElement.querySelector(".placeholder-wrapper").style.display = "none";
                        tag.style.display = "inline";
                    }, 300);
                    setTimeout(() => {
                        tag.style.display = "inline";
                        tag.style.opacity = "1";
                    }, 350);
                    tag.parentElement.querySelector(".placeholder-wrapper").style.opacity = "0";
                });
            });
        })
        .catch (error => {
            console.error(`Could not get converted versions of metadata urls.`);
            console.error(error);
        });
}

window.onload = convertOntologyServerUrlsAndResourceServerUrls;