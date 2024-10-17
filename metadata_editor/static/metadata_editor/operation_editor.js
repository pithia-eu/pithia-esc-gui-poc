import {
    editorForm,
    validateAndRegister,
} from "/static/metadata_editor/components/base_editor.js";
import {
    setupCitationSection,
} from "/static/metadata_editor/components/citation_section.js";
import {
    setupWizardManualAndAutoSave,
} from "/static/metadata_editor/components/editor_manual_and_autosave.js";
import {
    setupGeometryLocationSection,
} from "/static/metadata_editor/components/geometry_location_section.js";
import {
    setupRelatedPartiesTable,
} from "/static/metadata_editor/components/related_parties_table.js";
import {
    setupOperationTimeSection,
} from "/static/metadata_editor/components/operation/operation_time_section.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";

let relatedPartiesTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupWizardManualAndAutoSave();
    setupCitationSection();
    setupGeometryLocationSection();
    setupOperationTimeSection();
    setupTimePeriodElements("input[name='time_instant_begin_position']", "input[name='time_instant_end_position']");
    relatedPartiesTable = setupRelatedPartiesTable();
});