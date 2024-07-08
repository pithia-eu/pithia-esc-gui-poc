import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";

const instrumentSelect = document.querySelector("select[name='instrument_mode_pair_instrument']");
const instrumentModeSelect = document.querySelector("select[name='instrument_mode_pair_mode']");
const instrumentModeSelectOptGroups = Array.from(instrumentModeSelect.querySelectorAll("optgroup"));
const conditionalRequiredFields = [
    instrumentModeSelect,
];
const optionalFields = [
    instrumentSelect,
]


function filterInstrumentModeOptions(optGroupFilter) {
    if (!optGroupFilter) {
        for (const og of instrumentModeSelectOptGroups) {
            og.disabled = false;
        }
        instrumentModeSelect.disabled = true;
        window.dispatchEvent(new CustomEvent("selectDisabled", {
            detail: instrumentModeSelect.id,
        }));
    } else {
        for (const og of instrumentModeSelectOptGroups) {
            og.disabled = !(og.label === optGroupFilter);
        }
        instrumentModeSelect.disabled = false;
        window.dispatchEvent(new CustomEvent("selectEnabled", {
            detail: instrumentModeSelect.id,
        }));
    }
    window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
        detail: instrumentModeSelect.id,
    }));
}

function loadPreviousData() {
    if (instrumentSelect.value) {
        filterInstrumentModeOptions(instrumentSelect.options[instrumentSelect.selectedIndex].text);
    }
    checkAndSetRequiredAttributesForFields(conditionalRequiredFields, optionalFields);
}

export function setupInstrumentModePairSection() {
    loadPreviousData();

    instrumentSelect.addEventListener("change", () => {
        instrumentModeSelect.value = "";
        filterInstrumentModeOptions(instrumentSelect.options[instrumentSelect.selectedIndex].text);
        checkAndSetRequiredAttributesForFields(conditionalRequiredFields, optionalFields);
    });
}