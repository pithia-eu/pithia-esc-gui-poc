function setRequiredAttributesForFields(isRequired, fields) {
    for (const f of fields) {
        // Add/remove required class to/from
        // the field's label and corresponding
        // table headers
        let label = document.querySelector(`label[for="${f.id}"]`);
        let tsControl;
        if (f.classList.contains("tomselected")) {
            label = document.querySelector(`label[for="${f.id}-ts-control"]`);
            tsControl = document.querySelector(`input#${f.id}-ts-control`);
        }
        // Set required attribute
        if (!isRequired) {
            f.removeAttribute("required");
            if (label) label.classList.remove("required");
            if (tsControl) tsControl.classList.remove("required");
            continue;
        }
        f.setAttribute("required", true);
        if (label) label.classList.add("required");
        if (tsControl) tsControl.classList.add("required");
        // Reset any select "" value in case
        // it counts as a "selected" option.
        if (f.localName === "select" && f.value === "") {
            f.value = null;
        }
    }
}

export function checkAndConfigureRequiredAttributesOfSelects(selects) {
    if (!selects) {
        return;
    }
    const isRequired = !(selects.every(s => s.value === "")) || selects.every(s => s.value !== "");
    setRequiredAttributesForFields(isRequired, selects);
}

export function checkAndSetRequiredAttributesForFields(conditionalRequiredFields, optionalFields = []) {
    if (!conditionalRequiredFields) {
        return;
    }
    const allFields = [
        ...optionalFields,
        ...conditionalRequiredFields,
    ];
    const isRequiredAttributeSet = (allFields.some(f => !(f.value === "")));
    setRequiredAttributesForFields(isRequiredAttributeSet, conditionalRequiredFields);
}

export function checkAndSetRequiredAttributesForFieldsBySelectors(conditionalRequiredFieldsSelector, optionalRelatedFieldsSelector) {
    if (!conditionalRequiredFieldsSelector) {
        return;
    }
    const conditionalRequiredFields = document.querySelectorAll(conditionalRequiredFieldsSelector);
    const allFields = [
        ...document.querySelectorAll(optionalRelatedFieldsSelector),
        ...conditionalRequiredFields,
    ];
    const isRequiredAttributeSet = (allFields.some(f => !(f.value === "")));
    setRequiredAttributesForFields(isRequiredAttributeSet, conditionalRequiredFields);
}