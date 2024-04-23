import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupCitationSection,
} from "/static/register_with_support/components/citation_section.js";
import {
    setupGeometryLocationSection,
} from "/static/register_with_support/components/geometry_location_section.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupStandardIdentifiersTable,
} from "/static/register_with_support/components/platform/standard_identifiers_table.js";

let relatedPartiesTable;
let standardIdentifiersTable;


function prepareFormForSubmission() {
    relatedPartiesTable.exportTableDataToJsonAndStoreInOutputElement();
    standardIdentifiersTable.exportTableDataToJsonAndStoreInOutputElement();
}

editorForm.addEventListener("submit", async e => {
    e.preventDefault();

    prepareFormForSubmission();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupCitationSection();
    setupGeometryLocationSection();
    setupLocalIdAndNamespaceRelatedEventListeners();
    relatedPartiesTable = setupRelatedPartiesTable();
    standardIdentifiersTable = setupStandardIdentifiersTable();
});