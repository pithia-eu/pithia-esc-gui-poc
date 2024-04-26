const instrumentSelect = document.querySelector("select[name='instrument_mode_pair_instrument']");
const instrumentModesSelect = document.querySelector("select[name='instrument_mode_pair_mode']");
const instrumentModesSelectOptGroups = Array.from(instrumentModesSelect.querySelectorAll("optgroup"));


function filterInstrumentModeOptions(optGroupFilter) {
    if (!optGroupFilter) {
        for (const og of instrumentModesSelectOptGroups) {
            og.disabled = false;
        }
        instrumentModesSelect.disabled = true;
        window.dispatchEvent(new CustomEvent("selectDisabled", {
            detail: instrumentModesSelect.id,
        }));
    } else {
        for (const og of instrumentModesSelectOptGroups) {
            og.disabled = !(og.label === optGroupFilter);
        }
        instrumentModesSelect.disabled = false;
        window.dispatchEvent(new CustomEvent("selectEnabled", {
            detail: instrumentModesSelect.id,
        }));
    }
    window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
        detail: instrumentModesSelect.id,
    }));
}

function loadPreviousData() {
    if (instrumentSelect.value) {
        filterInstrumentModeOptions(instrumentSelect.options[instrumentSelect.selectedIndex].text);
    }
}

export function setupInstrumentModePairSection() {
    loadPreviousData();
}

instrumentSelect.addEventListener("change", () => {
    filterInstrumentModeOptions(instrumentSelect.options[instrumentSelect.selectedIndex].text);
});