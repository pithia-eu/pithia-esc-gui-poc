function setRequiredAttributesForFields(isRequired, fields) {
    for (const f of fields) {
        if (!isRequired) {
            f.removeAttribute("required");
            continue;
        }
        f.setAttribute("required", true);
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