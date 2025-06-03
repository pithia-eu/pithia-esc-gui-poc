const relatedMetadataUrl = JSON.parse(document.querySelector("#related-metadata-url").textContent);
const relatedMetadataNumber = document.querySelector("#related-metadata-num");
const relatedMetadataListPlaceholder = document.querySelector("#related-metadata-list-wrapper");


export async function loadRelatedMetadata() {
    if (!relatedMetadataUrl) {
        return;
    }
    const response = await fetch(relatedMetadataUrl);
    if (!response.ok) {
        const loadingErrorMessage = document.createElement("P");
        loadingErrorMessage.textContent = "Could not load related metadata.";
        relatedMetadataListPlaceholder.replaceWith(loadingErrorMessage);
    }
    const responseText = await response.text();
    relatedMetadataListPlaceholder.innerHTML = responseText;
    relatedMetadataNumber.textContent = `(${relatedMetadataListPlaceholder.querySelectorAll(".related-metadata-list-item").length})`;
}