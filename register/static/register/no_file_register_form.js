const inputSupportForm = document.getElementById("metadata-input-support-form");
const input = document.querySelector("#id_phone");

window.intlTelInput(input, {
    allowDropdown: false,
    autoPlaceholder: false,
    defaultToFirstCountry: false,
    nationalMode: false,
    placeholderNumberType: "FIXED_LINE",
    showFlags: false,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.4/build/js/utils.js",
});

async function validateAndRegister() {
    const formSubmitButton = inputSupportForm.querySelector("button[type='submit']");
    
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Validating</span>
    `;

    inputSupportForm.submit();
}

inputSupportForm.addEventListener("submit", async e => {
    e.preventDefault();

    // Enable required disabled inputs
    // Local ID
    const localIdInput = document.querySelector("input[name='localid']");
    localIdInput.disabled = false;

    // Namespace
    const namespaceInput = document.querySelector("input[name='namespace']");
    namespaceInput.disabled = false;

    validateAndRegister();
});
