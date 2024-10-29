function setupFormSubmitButtonSpinner() {
    const form = document.querySelector("#file-upload-form");
    const formSubmitButton = form.querySelector("button[type='submit']");
    const originalFormSubmitButtonText = formSubmitButton.textContent;
    formSubmitButton.disabled = true;
    form.addEventListener("submit", () => {
        formSubmitButton.innerHTML = `
            <span class="d-inline-flex align-items-center column-gap-2">
                <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
                <span role="status">${originalFormSubmitButtonText}</span>
            </span>
        `;
        formSubmitButton.disabled = true;
    });
}

window.addEventListener("load", () => {
    setupFormSubmitButtonSpinner();
});