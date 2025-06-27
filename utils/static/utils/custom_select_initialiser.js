const customSelects = {};
const selectControlWithNoSearchSelector = "select.no-search";
const keywordsInputSelector = "select[name='keyword']";
const userMenuInstitutionSelectControlSelector = ".user-dropdown select[name='institutions']";


function addEventListenersToCustomSelect(customSelect) {
    customSelect.control.addEventListener("mousedown", e => {
        if (document.activeElement.tagName !== "BODY") {
            document.activeElement.blur();
        }
    });
}

function addVisuallyHiddenClassToTomSelectControlInput(tomSelectInstance) {
    tomSelectInstance.control_input.classList.add("visually-hidden");
}

function removeVisuallyHiddenClassFromTomSelectControlInput(tomSelectInstance) {
    tomSelectInstance.control_input.classList.remove("visually-hidden");
}

function initialiseInstitutionSelectControlsInUserMenus(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            closeAfterSelect: true,
            maxOptions: null,
            onBlur: () => {
                removeVisuallyHiddenClassFromTomSelectControlInput(cs);
            },
            onDropdownClose: () => {
                addVisuallyHiddenClassToTomSelectControlInput(cs);
            },
            onType: () => {
                removeVisuallyHiddenClassFromTomSelectControlInput(cs);
            },
        });
        addEventListenersToCustomSelect(cs);
        customSelects[sc.id] = cs;
    });
}

function initialiseSelectControls(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            maxOptions: null,
        });
        addEventListenersToCustomSelect(cs);
        customSelects[sc.id] = cs;
    });
}

function initialiseSelectControlsWithNoSearch(selectControls) {
    selectControls.forEach(sc => {
        const cs = new TomSelect(sc, {
            controlInput: null,
        });
        addEventListenersToCustomSelect(cs);
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
        addEventListenersToCustomSelect(cs);
        customSelects[sc.id] = cs;
    });
}

// Initialise all selects on window load
window.addEventListener("load", () => {
    initialiseSelectControls(document.querySelectorAll(`select:not(${keywordsInputSelector}, ${selectControlWithNoSearchSelector}, ${userMenuInstitutionSelectControlSelector})`));
    initialiseSelectControlsWithNoSearch(document.querySelectorAll(`${selectControlWithNoSearchSelector}:not(${keywordsInputSelector}, ${userMenuInstitutionSelectControlSelector})`));
    initialiseInstitutionSelectControlsInUserMenus(document.querySelectorAll(userMenuInstitutionSelectControlSelector));
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