const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;

export function generateUniqueElemIdFromCurrentElemId(currentElemId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(currentElemId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${currentElemId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${currentElemId}${Date.now()}`;
}

export function getTableRowByChildNode(tableRowsContainer, childNode) {
    const tableRows = tableRowsContainer.querySelectorAll("tr");
    for (const row of tableRows) {
        if (row.contains(childNode)) {
            return row;
        }
    }
}

export function getNumRemainingRowsInTable(tableRowsContainer) {
    return tableRowsContainer.querySelectorAll("tr").length;
}