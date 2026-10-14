import {
    ServerURLConverter,
} from "/static/browse/server_url_conversion.js"


window.addEventListener("load", async () => {
    const serverUrlConverter = new ServerURLConverter({
        serverUrlElementSelector: ".resource-server-url",
        requestParamName: "resource-server-urls",
        propertyNameForConvertedUrls: "resource_urls"
    });
    await serverUrlConverter.convertServerUrlsToDetailPageUrlsAndDisplayInPage();
});