const customSelects = {};
const selectControlWithSearchSelector = "select:has(option:nth-child(6))";
const multipleChoiceSelectControlSelector = "select[multiple]";
const keywordsInputSelector = "select[name='keyword']";

function initialiseDefaultSelectControls(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {});
        customSelects[sc.id] = cs;
    });
}

function initialiseMultipleChoiceSelectControls(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            plugins: {
                checkbox_options: {
                    checkedClassNames: ["ts-checked"],
                    uncheckedClassNames: ["ts-unchecked"],
                }
            }
        });
        customSelects[sc.id] = cs;
    });
}

window.addEventListener("load", () => {
    initialiseDefaultSelectControls(document.querySelectorAll(`select:not(${keywordsInputSelector}, ${multipleChoiceSelectControlSelector})`));
    initialiseMultipleChoiceSelectControls(document.querySelectorAll(multipleChoiceSelectControlSelector));
});

window.addEventListener("newSelectsAdded", e => {
    const newSelectIds = e.detail;
    const newSelects = document.querySelectorAll(newSelectIds.map(id => `#${id}`).join(","));
    initialiseDefaultSelectControls(newSelects);
});

window.addEventListener("newMultipleChoiceSelectsAdded", e => {
    const newMultipleChoiceSelectIds = e.detail;
    const newMultipleChoiceSelects = document.querySelectorAll(newMultipleChoiceSelectIds.map(id => `#${id}`).join(","));
    initialiseMultipleChoiceSelectControls(newMultipleChoiceSelects);
});

window.addEventListener("selectOptionsSetProgrammatically", e => {
    const selectId = e.detail;
    customSelects[selectId].sync();
});