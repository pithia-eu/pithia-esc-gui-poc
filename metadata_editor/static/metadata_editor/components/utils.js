const RANDOM_STRING_PREFIX = "rs-";


// Credit: https://stackoverflow.com/a/1349426/10640126
function generateRandomString(length) {
    // Generates a random 5-character string.
    let result = "";
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    const charactersLength = characters.length;
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

export function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const randomStringLength = 5;
    const randomString = generateRandomString(randomStringLength);
    const randomStringWithPrefix = `${RANDOM_STRING_PREFIX}${randomString}`;
    const isRandomStringAlreadyAdded = currentElemId.slice(-randomStringWithPrefix).startsWith(RANDOM_STRING_PREFIX);
    if (isRandomStringAlreadyAdded) {
        return `${currentElemId.slice(0, -randomStringWithPrefix.length)}${randomStringWithPrefix}`
    }
    return `${currentElemId}${randomStringWithPrefix}`;
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
