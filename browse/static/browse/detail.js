const metadataServerUrlBase = "https://metadata.pithia.eu";

function getUrlToConvertServerUrlsBase() {
    return JSON.parse(document.getElementById("server-url-conversion-url").textContent);
}

function getConversionUrlForOntologyServerUrls(ontologyServerUrls) {
    const urlToConvertServerUrlsBase = getUrlToConvertServerUrlsBase();
    return `${urlToConvertServerUrlsBase}?ontology-server-urls=${ontologyServerUrls.join(",")}`;
}

function getConversionUrlForResourceServerUrls(resourceServerUrls) {
    const urlToConvertServerUrlsBase = getUrlToConvertServerUrlsBase();
    return `${urlToConvertServerUrlsBase}?resource-server-urls=${resourceServerUrls.join(",")}`;
}

function getServerUrlsToConvert() {
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
    return [ontologyServerUrls, resourceServerUrls, unknownServerUrls];
}

function getConversionUrlsWithFunction(serverUrls, conversionUrlFunction, conversionUrlsAndDetails) {
    function addConversionUrlAndDetails(conversionUrl, urlsToConvert) {
        conversionUrlsAndDetails.push({
            url: conversionUrl,
            urlsToConvert: urlsToConvert,
        })
    }

    if (serverUrls.length > 20) {
        let start = 0;
        while (start < serverUrls.length) {
            let end = start + 20;
            if (end > serverUrls.length) {
                end = serverUrls.length;
            }
            const urlsToConvert = serverUrls.slice(start, end);
            const conversionUrl = conversionUrlFunction(urlsToConvert);
            addConversionUrlAndDetails(conversionUrl, urlsToConvert);
            start += 20;
        }
    } else {
        const conversionUrl = conversionUrlFunction(serverUrls);
        addConversionUrlAndDetails(conversionUrl, serverUrls);
    }
    return conversionUrlsAndDetails;
}

function divideConversionUrlsForServerUrls(ontologyServerUrls, resourceServerUrls) {
    const allConversionUrlsAndDetails = [];
    if (ontologyServerUrls.length > 0) {
        const encodedOntologyServerUrls = ontologyServerUrls.map(url => encodeURIComponent(url));
        getConversionUrlsWithFunction(encodedOntologyServerUrls, getConversionUrlForOntologyServerUrls, allConversionUrlsAndDetails);
    }
    if (resourceServerUrls.length > 0) {
        const encodedResourceServerUrls = resourceServerUrls.map(url => encodeURIComponent(url));
        getConversionUrlsWithFunction(encodedResourceServerUrls, getConversionUrlForResourceServerUrls, allConversionUrlsAndDetails);
    }
    return allConversionUrlsAndDetails;
}

function addAnnotationToMetadataLink(text, element) {
    const smallText = document.createElement("small");
    smallText.innerHTML = text;
    smallText.className = "text-muted";
    element.parentElement.append(smallText);
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

function convertBatchOfOntologyServerUrlsAndResourceServerUrls(urlConversionDetails) {
    const conversionUrl = urlConversionDetails.url;
    const urlsToConvert = urlConversionDetails.urlsToConvert;
    const fetchParams = { method: "GET" };
    fetch(conversionUrl, fetchParams)
        .then(response => response.json())
        .then(responseContent => {
            const convertedOntologyUrlMappings = responseContent.ontology_urls;
            const convertedResourceUrlMappings = responseContent.resource_urls;

            // Checking whether some URLs have not been converted
            // before actually making changes to links in the page.
            const originalOntologyUrls = responseContent.ontology_urls.map(urlMapping => urlMapping.original_server_url);
            const originalResourceUrls = responseContent.resource_urls.map(urlMapping => urlMapping.original_server_url);

            urlsToConvert.forEach(encodedUrl => {
                const decodedUrl = decodeURIComponent(encodedUrl);
                if (!originalOntologyUrls.includes(decodedUrl) && !originalResourceUrls.includes(decodedUrl)) {
                    const metadataLinkTag = document.querySelector(`a[href="${decodedUrl}"]`);
                    if (metadataLinkTag !== null) {
                        revealMetadataLink(metadataLinkTag);
                    }
                }
            });

            convertedOntologyUrlMappings.forEach(urlMapping => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${urlMapping.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = urlMapping.converted_url;
                    tag.innerHTML = urlMapping.converted_url_text;
                    revealMetadataLink(tag);
                });
            });

            convertedResourceUrlMappings.forEach(urlMapping => {
                const anchorTagsWithUrl = document.querySelectorAll(`a[href="${urlMapping.original_server_url}"]`);
                anchorTagsWithUrl.forEach(tag => {
                    tag.href = urlMapping.converted_url;
                    tag.innerHTML = urlMapping.converted_url_text;
                    revealMetadataLink(tag);
                });
            });
        })
        .catch (error => {
            console.error(`Could not get converted versions of metadata urls.`);
            console.error(error);
            urlsToConvert.forEach(encodedUrl => {
                const decodedUrl = decodeURIComponent(encodedUrl);
                const metadataLinkTags = document.querySelectorAll(`a[href="${decodedUrl}"]:not([style*="display: inline"])`);
                metadataLinkTags.forEach(metadataLinkTag => {
                    const decodedUrlSplit = decodedUrl.split("/");
                    metadataLinkTag.innerHTML = decodedUrlSplit[decodedUrlSplit.length - 1];
                    revealMetadataLink(metadataLinkTag);
                });
            });
        });
}

function convertAllOntologyServerUrlsAndResourceServerUrls() {
    const [ontologyServerUrls, resourceServerUrls, unknownServerUrls] = getServerUrlsToConvert();
    if ((ontologyServerUrls.length + resourceServerUrls.length) === 0) {
        return;
    }
    const conversionUrlsAndUrlsToConvert = divideConversionUrlsForServerUrls(ontologyServerUrls, resourceServerUrls);
    conversionUrlsAndUrlsToConvert.forEach(urlConversionDetails => {
        convertBatchOfOntologyServerUrlsAndResourceServerUrls(urlConversionDetails);
    });
}

window.onload = convertAllOntologyServerUrlsAndResourceServerUrls;