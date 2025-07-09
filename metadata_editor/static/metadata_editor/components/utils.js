const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

export function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
}

export function updateDuplicatedElemsWithIdsInContainer(elems, containerElement) {
    elems.forEach(elem => {
        if (elem.classList.contains("field-wrapper") || elem.classList.contains("invalid-feedback")) {
            return;
        }
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const invalidFeedbackElements = containerElement.querySelectorAll(`.invalid-feedback[data-field="${elem.id}"]`);
        const fieldWrappers = containerElement.querySelectorAll(`.field-wrapper[data-field="${elem.id}"]`);
        const correspondingLabels = containerElement.querySelectorAll(`label[for="${elem.id}"]`);
        const correspondingAriaDescBys = containerElement.querySelectorAll(`[aria-describedby="${elem.id}"]`);
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
        correspondingAriaDescBys.forEach(correspondingAriaDescBy => {
            correspondingAriaDescBy.setAttribute("aria-describedby", newId);
        });
        invalidFeedbackElements.forEach(invalidFeedbackElem => {
            const newInvalidFeedbackElemId = `invalid-feedback-${newId}`;
            if (elem.getAttribute("aria-describedby") === invalidFeedbackElem.id) {
                elem.setAttribute("aria-describedby", newInvalidFeedbackElemId);
            }
            invalidFeedbackElem.setAttribute("data-field", newId);
            invalidFeedbackElem.setAttribute("id", newInvalidFeedbackElemId);
        });
        fieldWrappers.forEach(fieldWrapper => {
            const newFieldWrapperId = `field-wrapper-${newId}`;
            fieldWrapper.setAttribute("data-field", newId);
            fieldWrapper.setAttribute("id", newFieldWrapperId);
        });
    });
}
