const foiSearchForm = document.querySelector("#foi-search-form");
const dataCollectionCountsByFoi = JSON.parse(document.querySelector("#data-collection-counts-by-foi").textContent);
const foiSearchButtons = document.querySelectorAll(".btn-foi-search");


function getLocalIdFromFoiUrl(foiUrl) {
    return foiUrl.split("/").pop();
}

function populateAndSubmitFoiSearchForm(foiUrls) {
    foiUrls.forEach(foiUrl => {
        const foiLocalId = getLocalIdFromFoiUrl(foiUrl);
        const input = document.createElement("INPUT");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", "featureOfInterest");
        input.value = foiLocalId;
        foiSearchForm.appendChild(input);
    });
    return foiSearchForm.submit();
}

foiSearchButtons.forEach(foiSearchButton => {
    foiSearchButton.addEventListener("click", () => {
        const foiUrl = foiSearchButton.dataset.foiUrl;
        const foiDescendents = dataCollectionCountsByFoi[foiUrl].descendents;
        populateAndSubmitFoiSearchForm([
            foiUrl,
            ...foiDescendents,
        ]);
    });
});