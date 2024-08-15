import {
    ServerURLConverter,
} from "/static/browse/server_url_conversion.js"


window.addEventListener("load", async () => {
    const serverUrlConverter = new ServerURLConverter(
        "ontology-server-url",
        "ontology-server-urls",
        "ontology_urls"
    );
    await serverUrlConverter.convertServerUrlsToDetailPageUrlsAndDisplayInPage();
});