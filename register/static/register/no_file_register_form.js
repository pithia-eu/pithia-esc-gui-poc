export const inputSupportForm = document.getElementById("metadata-input-support-form");
export const inputSupportFormSubmitButton = document.getElementById("metadata-input-support-form");

export async function validateAndRegister() {
    const formSubmitButton = inputSupportForm.querySelector("button[type='submit']");
    
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Validating</span>
    `;

    inputSupportForm.submit();
}

export function enableLocalIdAndNamespaceFields() {
    // Enable required disabled inputs
    // Local ID
    const localIdInput = document.querySelector("input[name='localid']");
    localIdInput.disabled = false;

    // Namespace
    const namespaceInput = document.querySelector("input[name='namespace']");
    namespaceInput.disabled = false;
}
