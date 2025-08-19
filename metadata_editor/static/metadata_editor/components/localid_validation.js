const localIdValidationUrl = JSON.parse(document.getElementById("local-id-validation-url").textContent);

export async function checkLocalIdIsUnique(localId) {
    let localIdCheck = {};
    if (!localIdValidationUrl || localIdValidationUrl.length === 0) {
        const msg = "Cannot check local ID as no validation URL supplied.";
        console.log(msg);
        localIdCheck.error = msg;
        localIdCheck.displayError = true;
        return localIdCheck;
    }

    let response;
    try {
        response = await fetch(`${localIdValidationUrl}?` + new URLSearchParams({
            localid: localId
        }));
        const responseBody = await response.json();
        localIdCheck = {
            ...localIdCheck,
            ...responseBody,
        };
    } catch (error) {
        const msg = "Encountered an error checking local ID for uniqueness.";
        console.error(error);
        console.log(msg);
        if (response) console.error(`Response:`, response);
        localIdCheck.error = `${msg} Please try again later.`;
        localIdCheck.displayError = true;
    }
    return localIdCheck;
}