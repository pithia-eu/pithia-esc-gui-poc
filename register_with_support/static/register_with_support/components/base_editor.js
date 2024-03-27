export const editorForm = document.getElementById("metadata-editor-form");

export async function validateAndRegister() {
    const formSubmitButton = editorForm.querySelector("button[type='submit']");
    
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Validating</span>
    `;

    editorForm.submit();
}
