function titleCaseString(inputString) {
    const inputStringSplit = inputString.split(" ");
    for (let i = 0; i < inputStringSplit.length; i++) {
        inputStringSplit[i] = inputStringSplit[i].charAt(0).toUpperCase() + inputStringSplit[i].slice(1);
    }
    return inputStringSplit.join(" ");
}

function strip(html) {
    const doc = new DOMParser().parseFromString(html, "text/html");
    return doc.body.textContent || '';
}

export function cleanLocalId(localId) {
    return encodeURIComponent(strip(localId).replace(/[^a-zA-Z0-9 \-\_]/g, ""));
}

export function generateLocalId(name) {
    return cleanLocalId(titleCaseString(name).replace(/\s/g, "_"));
}