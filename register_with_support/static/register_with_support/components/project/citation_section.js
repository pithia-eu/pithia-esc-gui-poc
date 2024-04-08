import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/project/conditional_required_fields.js";
const citationSection = editorForm.querySelector("#citation-section");
const citationSectionRequiredFieldsSelector = "input[name='citation_title'], input[name='citation_publication_date']";
const citationSectionFields = citationSection.querySelectorAll("input, textarea");
const citationSectionRequiredFields = Array.from(citationSection.querySelectorAll(citationSectionRequiredFieldsSelector));
const citationSectionOptionalFields = Array.from(citationSection.querySelectorAll(`input:not(${citationSectionRequiredFieldsSelector}), textarea`));


function setRequiredAttributesForConditionalRequiredFields() {
    checkAndSetRequiredAttributesForFields(
        citationSectionRequiredFields,
        citationSectionOptionalFields,
    );
}

export function setupCitationSection() {
    // The citation title and date fields only
    // become required when other citation
    // fields are filled in.

    // Do initial setup in case there are already
    // some initial values in the form
    setRequiredAttributesForConditionalRequiredFields();

    // Set event listeners for each field in the
    // citation section
    citationSectionFields.forEach(field => {
        field.addEventListener("input", () => {
            setRequiredAttributesForConditionalRequiredFields();
        });
    });
}