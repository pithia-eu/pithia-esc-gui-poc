export const editorForm = document.getElementById("metadata-editor-form");
const xmlGenerationUrl = JSON.parse(document.getElementById("xml-generation-url").textContent);
// Form submit button animation
const formSubmitButton = editorForm.querySelector("button[type='submit']");
const formSubmitButtonDefaultContent = formSubmitButton.innerHTML;
// Form submission status
const formStatusAlert = document.querySelector(".form-status-alert");
// Form submit abort button
const formCancelButton = editorForm.querySelector(".btn-abort-submit");
let controller;
// Network error msg
const NETWORK_ERROR_MSG = "The connection to the server timed out before validation could finish. Please try submitting the form again."


function updateFormStatusAlert(content) {
    formStatusAlert.textContent = content;
    return formStatusAlert.classList.remove("d-none");
}

function showInProgressAnimationAndContent() {
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Validating</span>
    `;
    formCancelButton.classList.remove("d-none");
}

function stopInProgressAnimationAndContent() {
    formSubmitButton.innerHTML = formSubmitButtonDefaultContent;
    formSubmitButton.disabled = false;
    formCancelButton.classList.add("d-none");
}

function showSuccessAnimationAndContent() {
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Redirecting</span>
    `;
    formCancelButton.disabled = true;
}

export async function validateAndRegister() {
    controller = new AbortController();

    // Hide form status alert if visible
    formStatusAlert.classList.add("d-none");

    // Show submit button "in-progress" animation
    showInProgressAnimationAndContent();

    // Submit form asynchronously
    let responseJson;
    let isResponseComplete;
    try {
        const url = `${window.location.origin}${xmlGenerationUrl}`;
        const data = new URLSearchParams(new FormData(editorForm));
        const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        data.append("csrfmiddlewaretoken", csrfMiddlewareToken);
        const response = await fetch(url, {
            method: "POST",
            body: data,
            signal: controller.signal,
        });
        isResponseComplete = true;

        if (response.status === 504) {
            updateFormStatusAlert(NETWORK_ERROR_MSG);
            throw new Error(`Response status: ${response.status}`);
        }

        if (!response.ok) {
            updateFormStatusAlert(await response.text());
            throw new Error(`Response status: ${response.status}`);
        }
        responseJson = await response.json();
        editorForm.setAttribute("action", responseJson.redirect_url);
    } catch (error) {
        console.error(error.message);
        if (!isResponseComplete) {
            updateFormStatusAlert(NETWORK_ERROR_MSG);
        }
        return stopInProgressAnimationAndContent();
    } finally {
        controller = null;
    }

    showSuccessAnimationAndContent();
    return editorForm.submit();
}

formCancelButton.addEventListener("click", () => {
    if (controller) {
        controller.abort();
        return stopInProgressAnimationAndContent();
    }
    console.log("There is no active request.");
    return stopInProgressAnimationAndContent();
});