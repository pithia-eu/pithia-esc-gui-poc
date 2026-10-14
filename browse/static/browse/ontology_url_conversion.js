import {
    ServerURLConverter,
} from "/static/browse/server_url_conversion.js"


window.addEventListener("load", async () => {
    const serverUrlConverter = new ServerURLConverter({
        serverUrlElementSelector: ".ontology-server-url",
        requestParamName: "ontology-server-urls",
        propertyNameForConvertedUrls: "ontology_urls"
    });
    await serverUrlConverter.convertServerUrlsToDetailPageUrlsAndDisplayInPage();
});