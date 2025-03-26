export const editorForm = document.getElementById("metadata-editor-form");

// export async function validateAndRegister() {
//     const formSubmitButton = editorForm.querySelector("button[type='submit']");
    
//     formSubmitButton.disabled = true;
//     formSubmitButton.innerHTML = `
//         <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
//         <span role="status">Validating</span>
//     `;

//     editorForm.submit();
// }

export async function validateAndRegister() {
    // Hide form status alert if visible
    const formStatusAlert = document.querySelector(".form-status-alert");
    formStatusAlert.classList.add("d-none");

    // Show submit button "in-progress" animation
    const formSubmitAbortButton = editorForm.querySelector(".btn-abort-submit");
    const formSubmitButton = editorForm.querySelector("button[type='submit']");
    const formSubmitButtonDefaultContent = formSubmitButton.innerHTML;
    formSubmitButton.disabled = true;
    formSubmitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
        <span role="status">Validating</span>
    `;
    formSubmitAbortButton.classList.remove("d-none");

    // Submit form asynchronously
    const editorFormAction = editorForm.getAttribute("action");
    const responseContent = {
        type: "default",
        text: "",
    };
    try {
        const url = `${window.location.origin}${editorFormAction}`;
        const data = new URLSearchParams(new FormData(editorForm));
        const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        data.append("csrfmiddlewaretoken", csrfMiddlewareToken);
        const response = await fetch(url, {
            method: "POST",
            body: data,
        });
        if (!response.ok) {
            responseContent.type = "error";
            responseContent.text = await response.text();
            formStatusAlert.textContent = responseContent.text;
            formStatusAlert.classList.remove("d-none");
            throw new Error(`Response status: ${response.status}`);
        }
        responseContent.text = await response.text();
    } catch (error) {
        console.error(error.message);
        formSubmitButton.innerHTML = formSubmitButtonDefaultContent;
        formSubmitButton.disabled = false;
        formSubmitAbortButton.classList.add("d-none");
        return responseContent;
    }

    return window.location.replace(`${window.location.href.split("?")[0]}?reset=true&success=true`);
}