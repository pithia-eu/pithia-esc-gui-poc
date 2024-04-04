const selectControlWithSearchSelector = "select:has(option:nth-child(6))";
const keywordsInputSelector = "select[name='keyword']";

function initialiseDefaultSelectControls(selectControls) {
    selectControls.forEach(el => {
        new TomSelect(el, {});
    });
}

window.addEventListener("load", () => {
    initialiseDefaultSelectControls(document.querySelectorAll(`select:not(${keywordsInputSelector})`));
});