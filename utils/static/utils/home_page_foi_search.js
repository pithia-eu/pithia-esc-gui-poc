const foiSearchForm = document.querySelector("#foi-search-form");
const dataCollectionCountsByFoi = JSON.parse(document.querySelector("#data-collection-counts-by-foi").textContent);
const foiSearchButtons = document.querySelectorAll(".btn-foi-search");


function getLocalIdFromFoiUrl(foiUrl) {
    return foiUrl.split("/").pop();
}

function resetFoiSearchForm() {
    const previousSearchInputs = foiSearchForm.querySelectorAll(".foi-search-input");
    previousSearchInputs.forEach(input => {
        return input.remove();
    });
}

function populateAndSubmitFoiSearchForm(foiUrls) {
    foiUrls.forEach(foiUrl => {
        const foiLocalId = getLocalIdFromFoiUrl(foiUrl);
        const input = document.createElement("INPUT");
        input.setAttribute("type", "hidden");
        input.setAttribute("name", "featureOfInterest");
        input.classList.add("foi-search-input");
        input.value = foiLocalId;
        foiSearchForm.appendChild(input);
    });
    return foiSearchForm.submit();
}

foiSearchButtons.forEach(foiSearchButton => {
    foiSearchButton.addEventListener("click", () => {
        resetFoiSearchForm();
        const foiUrl = foiSearchButton.dataset.foiUrl;
        const foiDescendents = dataCollectionCountsByFoi[foiUrl].descendents;
        populateAndSubmitFoiSearchForm([
            foiUrl,
            ...foiDescendents,
        ]);
    });
});