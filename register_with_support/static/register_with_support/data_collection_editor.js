import {
    editorForm,
    validateAndRegister,
} from "/static/register_with_support/components/base_editor.js";
import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/register_with_support/components/localid_validation.js";
import {
    setupQualityAssessmentSection,
} from "/static/register_with_support/components/quality_assessment.js";
import {
    setupRelatedPartiesTable,
} from "/static/register_with_support/components/related_parties_table.js";
import {
    setupSourcesTab,
} from "/static/register_with_support/components/sources_tab.js";

editorForm.addEventListener("submit", e => {
    e.preventDefault();

    validateAndRegister();
});

window.addEventListener("load", () => {
    setupLocalIdAndNamespaceRelatedEventListeners();
    const sourcesTab = setupSourcesTab();
    const relatedPartiesTable = setupRelatedPartiesTable();
    setupQualityAssessmentSection();
});