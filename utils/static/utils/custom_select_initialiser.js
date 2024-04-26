const customSelects = {};
const selectControlWithNoSearchSelector = "select.no-search";
const keywordsInputSelector = "select[name='keyword']";

function initialiseSelectControls(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {});
        customSelects[sc.id] = cs;
    });
}

function initialiseSelectControlsWithNoSearch(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            controlInput: null,
        });
        customSelects[sc.id] = cs;
    });
}

function initialiseKeywordMultipleChoiceSelectControls(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            create: true,
            persist: false,
            render: {
                no_results: null,
            }
        });
        customSelects[sc.id] = cs;
    });
}

// Initialise all selects on window load
window.addEventListener("load", () => {
    initialiseSelectControls(document.querySelectorAll(`select:not(${keywordsInputSelector}, ${selectControlWithNoSearchSelector})`));
    initialiseSelectControlsWithNoSearch(document.querySelectorAll(`${selectControlWithNoSearchSelector}:not(${keywordsInputSelector})`));
    initialiseKeywordMultipleChoiceSelectControls(document.querySelectorAll(`${keywordsInputSelector}`));
});

// Custom event listeners
window.addEventListener("newSelectsAdded", e => {
    const newSelectIds = e.detail;
    const newSelects = document.querySelectorAll(newSelectIds.map(id => `#${id}`).join(","));
    initialiseSelectControls(newSelects);
});

window.addEventListener("newMultipleChoiceSelectsAdded", e => {
    const newMultipleChoiceSelectIds = e.detail;
    const newMultipleChoiceSelects = document.querySelectorAll(newMultipleChoiceSelectIds.map(id => `#${id}`).join(","));
    initialiseSelectControls(newMultipleChoiceSelects);
});

window.addEventListener("newKeywordsSelectsAdded", e => {
    const newKeywordsSelectIds = e.detail;
    const newKeywordsSelects = document.querySelectorAll(newKeywordsSelectIds.map(id => `#${id}`).join(","));
    initialiseKeywordMultipleChoiceSelectControls(newKeywordsSelects);
});

window.addEventListener("selectOptionsSetProgrammatically", e => {
    const selectId = e.detail;
    customSelects[selectId].sync();
});

window.addEventListener("selectDisabled", e => {
    const selectId = e.detail;
    customSelects[selectId].disable();
});

window.addEventListener("selectEnabled", e => {
    const selectId = e.detail;
    customSelects[selectId].enable();
});