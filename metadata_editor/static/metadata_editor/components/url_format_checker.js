export function checkIfEscUrl(urlText) {
    const urlToCheck = new URL(urlText);
    return urlToCheck.hostname == 'esc.pithia.eu';
}