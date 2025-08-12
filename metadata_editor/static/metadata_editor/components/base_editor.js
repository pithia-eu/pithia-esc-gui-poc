export const editorForm = document.getElementById("metadata-editor-form");


export class BaseEditor {
    setup() {
        this.setupClassVariables();
        this.setupEventListeners();
        this.setupValidator();
    }

    setupClassVariables() {
        this.editorForm = editorForm;
        this.xmlGenerationUrl = JSON.parse(document.getElementById("xml-generation-url").textContent);
        // Form submit button animation
        this.formSubmitButton = this.editorForm.querySelector("button[type='submit']");
        this.formSubmitButtonDefaultContent = this.formSubmitButton.innerHTML;
        // Form submission status
        this.formStatusAlert = document.querySelector(".form-status-alert");
        // Form submit abort button
        this.formRetryNotice = document.querySelector(".form-retry-notice");
        this.formCancelButton = this.editorForm.querySelector(".btn-abort-submit");
        this.controller = null;
        this.isRequestAborted = false;
        // Error messages
        this.NETWORK_ERROR_MSG = "The connection to the server timed out. Please try submitting the form again, and if the problem persists please let our support team know.";
    }

    setupEventListeners() {
        this.formCancelButton.addEventListener("click", () => {
            if (this.controller) {
                this.isRequestAborted = true;
                this.controller.abort();
                return this.stopInProgressAnimationAndContent();
            }
            console.log("There is no active request.");
            return this.stopInProgressAnimationAndContent();
        });

        editorForm.addEventListener("submit", async e => {
            e.preventDefault();
            await this.submitAndGenerateXml();
        });
    }

    getValidator() {
    }

    setupValidator() {
        this.validator = this.getValidator();
        if (!this.validator) {
            return;
        }
        this.validator.setup();
    }

    async runAfterInitialEditorSetup() {
    }

    getFieldsToValidateOnInput() {
        return this.editorForm.querySelectorAll("input:not(input[type='email']), textarea");
    }

    getFieldsToValidateOnBlur() {
        return this.editorForm.querySelectorAll("input[type='email']");
    }

    getSelectsToValidateOnInput() {
        return this.editorForm.querySelectorAll("select");
    }

    updateFormStatusAlert(content) {
        this.formStatusAlert.textContent = content;
        return this.formStatusAlert.classList.remove("d-none");
    }
    
    showInProgressAnimationAndContent() {
        this.formSubmitButton.disabled = true;
        this.formSubmitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
            <span role="status">Validating</span>
        `;
        this.formRetryNotice.classList.remove("d-none");
    }
    
    stopInProgressAnimationAndContent() {
        this.formSubmitButton.innerHTML = this.formSubmitButtonDefaultContent;
        this.formSubmitButton.disabled = false;
        this.formRetryNotice.classList.add("d-none");
    }
    
    showSuccessAnimationAndContent() {
        this.formSubmitButton.disabled = true;
        this.formSubmitButton.classList.remove('btn-outline-primary');
        this.formSubmitButton.classList.add('btn-outline-secondary');
        this.formSubmitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-1" aria-hidden="true"></span>
            <span role="status">Redirecting</span>
        `;
        this.formCancelButton.disabled = true;
    }

    displayFormErrors(formErrors) {
        for (const fieldName in formErrors) {
            console.log(fieldName, formErrors[fieldName]);
        }
    }

    processResponseTextIfJson(responseText) {
        try {
            const data = JSON.parse(responseText);
            this.displayFormErrors(data.errors);
            this.updateFormStatusAlert(data.message);
            return {success: true};
        } catch (error) {
            // Response was not a JSON object, continue
            // with default response handling.
            console.error("Could not display form validation errors.", error);
        }
        return {success: false};
    }
    
    async submitAndGenerateXml() {
        this.controller = new AbortController();
        this.isRequestAborted = false;
    
        // Hide form status alert if visible
        this.formStatusAlert.classList.add("d-none");
    
        // Show submit button "in-progress" animation
        this.showInProgressAnimationAndContent();
    
        // Submit form asynchronously
        let responseJson;
        let isResponseComplete;
        try {
            const url = `${window.location.origin}${this.xmlGenerationUrl}`;
            let data = new FormData(this.editorForm);
            if (this.editorForm.getAttribute("enctype") !== "multipart/form-data") {
                data = new URLSearchParams(data);
            }
            const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
            data.append("csrfmiddlewaretoken", csrfMiddlewareToken);
            const response = await fetch(url, {
                method: "POST",
                body: data,
                signal: this.controller.signal,
            });
            isResponseComplete = true;
            
            if (response.status === 504) {
                this.updateFormStatusAlert(this.NETWORK_ERROR_MSG);
                throw new Error(`Response status: ${response.status}`);
            }
    
            if (!response.ok) {
                const responseText = await response.text();
                const processingResults = this.processResponseTextIfJson(responseText);
                if (processingResults.success) {
                    throw new Error(`Response status: ${response.status}`);
                }
                if (responseText.toLowerCase().startsWith("<!doctype html>")) {
                    this.updateFormStatusAlert("An unexpected response was received. Please try submitting the form again. If the problem persists, please let our support team know.");
                    throw new Error(`Response status: ${response.status}`);
                }
                this.updateFormStatusAlert(responseText);
                throw new Error(`Response status: ${response.status}`);
            }
            responseJson = await response.json();
            this.editorForm.setAttribute("action", responseJson.redirect_url);
        } catch (error) {
            console.error(error.message);
            if (this.isRequestAborted) {
                return this.stopInProgressAnimationAndContent();
            }
            if (!isResponseComplete) {
                this.updateFormStatusAlert(this.NETWORK_ERROR_MSG);
            }
            return this.stopInProgressAnimationAndContent();
        } finally {
            this.controller = null;
        }
    
        window.dispatchEvent(new CustomEvent("xmlRegisteredSuccessfully"));
        this.showSuccessAnimationAndContent();
        return this.editorForm.submit();
    }
}