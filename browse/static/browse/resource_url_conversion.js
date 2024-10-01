import {
    ServerURLConverter,
} from "/static/browse/server_url_conversion.js"


window.addEventListener("load", async () => {
    const serverUrlConverter = new ServerURLConverter(
        "resource-server-url",
        "resource-server-urls",
        "resource_urls"
    );
    await serverUrlConverter.convertServerUrlsToDetailPageUrlsAndDisplayInPage();
});