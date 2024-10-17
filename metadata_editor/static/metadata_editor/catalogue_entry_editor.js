import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";


editorForm.addEventListener("submit", async e => {
    e.preventDefault();
    await validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
});