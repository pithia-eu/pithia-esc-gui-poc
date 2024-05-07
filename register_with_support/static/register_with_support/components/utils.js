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
        const newId = generateUniqueElemIdFromCurrentElemId(elem.id);
        const correspondingLabels = containerElement.querySelectorAll(`label[for="${elem.id}"]`);
        const correspondingAriaDescBys = containerElement.querySelectorAll(`[aria-describedby="${elem.id}"]`);
        elem.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
        correspondingAriaDescBys.forEach(elem => {
            elem.setAttribute("aria-describedby", newId);
        });
    });
}
