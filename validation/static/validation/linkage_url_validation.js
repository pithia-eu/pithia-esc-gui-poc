export function checkIfEscUrl(urlText) {
    const urlToCheck = new URL(urlText);
    return urlToCheck.hostname == 'esc.pithia.eu';
}

export function checkLinkageUrlIsValid(linkageUrl) {
    try {
        const isLinkageUrlInternal = checkIfEscUrl(linkageUrl);
        if (isLinkageUrlInternal) {
            return {
                valid: false,
                error: "urlIsInternal",
            }
        }
    } catch (error) {
        console.error(error);
        return {
            valid: false,
            error: "urlSyntaxIsInvalid",
        };
    }
    return {
        valid: true,
    };
}