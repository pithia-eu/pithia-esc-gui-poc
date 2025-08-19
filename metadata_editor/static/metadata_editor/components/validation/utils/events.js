export function dispatchValidateFieldsEvent(fields) {
    window.dispatchEvent(new CustomEvent("validateFields", {
        detail: {
            fieldIds: fields.map(field => field.id),
        }
    }));
}

