const selectControlWithSearchSelector = "select:has(option:nth-child(6))";
const keywordsInputSelector = "select[name='keyword']";

function initialiseDefaultSelectControls(selectControls) {
    selectControls.forEach(el => {
        new TomSelect(el, {});
    });
}

function initialiseKeywordsInput(keywordsInput) {
    new TomSelect(keywordsInput, {
        create: true,
        persist: false,
        render: {
            no_results: null,
        },
    });
}

window.addEventListener("load", () => {
    initialiseDefaultSelectControls(document.querySelectorAll(`select:not(${keywordsInputSelector})`));
    initialiseKeywordsInput(document.querySelector(keywordsInputSelector));
});