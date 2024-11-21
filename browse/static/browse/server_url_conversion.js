const CONVERSION_URL = JSON.parse(document.getElementById("server-url-conversion-url").textContent);


export class ServerURLConverter {
    constructor(serverUrlElementClassSelector, requestParamName, responseUrlsKey) {
        this.serverUrlElementClassSelector = serverUrlElementClassSelector;
        this.requestParamName = requestParamName;
        this.responseUrlsKey = responseUrlsKey;
    }
    
    getURLsToConvert() {
        const elementsWithUrls = Array.from(document.querySelectorAll(`.${this.serverUrlElementClassSelector}[data-metadata-server-url]`));
        return Array.from(new Set(elementsWithUrls.map(e => e.dataset.metadataServerUrl)));
    }
    
    async getResourceServerUrlToDetailPageUrlMappings(urls) {
        try {
            const formData = new FormData();
            formData.append(this.requestParamName, JSON.stringify(urls));
            formData.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
            const response = await fetch(`${CONVERSION_URL}`, {
                method: "POST",
                body: formData,
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }
    
            const json = await response.json();
            return json[this.responseUrlsKey];
        } catch (error) {
            console.error(error);
        }
        return [];
    }
    
    swapAnchorElementUrlsWithConvertedUrlInPage(originalServerUrl, convertedUrl, convertedUrlText) {
        const anchorContainerElements = document.querySelectorAll(`.${this.serverUrlElementClassSelector}[data-metadata-server-url="${originalServerUrl}"]`);
        for (const e of anchorContainerElements) {
            const metadataUrlTextElement = e.querySelector(".metadata-server-url-text");
            metadataUrlTextElement.textContent = convertedUrlText;
            metadataUrlTextElement.href = convertedUrl;
            this.showElementWithConvertedUrlInPage(e);
        }
    }
    
    showElementWithConvertedUrlInPage(element) {
        element.classList.remove("loading");
    }

    async convertServerUrlsToDetailPageUrlsAndDisplayInPage() {
        const urls = this.getURLsToConvert();
        const urlMappings = await this.getResourceServerUrlToDetailPageUrlMappings(urls);
        for (const urlMapping of urlMappings) {
            this.swapAnchorElementUrlsWithConvertedUrlInPage(
                urlMapping.original_server_url,
                urlMapping.converted_url,
                urlMapping.converted_url_text
            );
        }
        const remainingElements = document.querySelectorAll(`.${this.serverUrlElementClassSelector}[data-metadata-server-url].loading`);
        for (const e of remainingElements) {
            this.showElementWithConvertedUrlInPage(e);
        }
    }
}