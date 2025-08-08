import {
    updateDuplicatedElemsWithIdsInContainer,
} from "/static/metadata_editor/components/utils.js";


export const phoneInput = document.querySelector("#id_phone");
// Initialise phone number input auto-formatting
export const iti = window.intlTelInput(phoneInput, {
    allowDropdown: false,
    autoPlaceholder: false,
    defaultToFirstCountry: false,
    nationalMode: false,
    placeholderNumberType: "FIXED_LINE",
    showFlags: false,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.5.4/build/js/utils.js",
});


class EmailAddressContactInfoSection {
    constructor() {
        this.emailAddressInputList = document.querySelector("#email-address-input-list");
        this.emailAddressFieldTemplate = JSON.parse(document.querySelector("#email-address-field-template").textContent);
        this.emailAddressInputSelector = "input[name='email_address']";
        this.removeEmailAddressInputButtonSelector = "button.btn-remove-email"
        this.emailAddressesJsonOutputElement = document.querySelector("input[name='email_addresses_json']");
        this.addEmailAddressInputButton = document.querySelector("#add-email-address-btn");
    }

    setup() {
        const firstLiElement = this.emailAddressInputList.querySelector("li");
        this.setupEmailAddressInputEventListeners(firstLiElement);
        this.loadPreviousData();
        this.setupAddEmailAddressInputButton();
        this.disableFirstRemoveEmailInputButtonIfOnlyOne();
    }
    
    setupEmailAddressInputEventListeners(containingLiElement) {
        const emailAddressInput = containingLiElement.querySelector(this.emailAddressInputSelector);
        emailAddressInput.addEventListener("input", () => {
            this.exportEmailAddressesToJsonOutputElement();
        });
        const removeEmailAddressInputButton = containingLiElement.querySelector(this.removeEmailAddressInputButtonSelector);
        removeEmailAddressInputButton.addEventListener("click", () => {
            this.removeEmailAddressInput(containingLiElement);
            this.exportEmailAddressesToJsonOutputElement();
        });
    }

    setupAddEmailAddressInputButton() {
        this.addEmailAddressInputButton.addEventListener("click", () => {
            this.addEmailAddressInput();
            this.exportEmailAddressesToJsonOutputElement();
        });
    }

    disableFirstRemoveEmailInputButtonIfOnlyOne() {
        const firstRemoveEmailAddressInputButton = this.emailAddressInputList.querySelector(this.removeEmailAddressInputButtonSelector);
        firstRemoveEmailAddressInputButton.disabled = this.emailAddressInputList.children.length === 1;
    }

    updateDuplicatedContentInNewLiElement(newLiElement) {
        const childElementsWithId = newLiElement.querySelectorAll("[id]");
        updateDuplicatedElemsWithIdsInContainer(childElementsWithId, newLiElement);
    }

    removeEmailAddressInput(containingLiElement) {
        containingLiElement.remove();
        this.disableFirstRemoveEmailInputButtonIfOnlyOne();
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallyRemoved"));
    }

    addEmailAddressInput() {
        const newLiElement = document.createElement("LI");
        newLiElement.innerHTML = this.emailAddressFieldTemplate;
        this.setupEmailAddressInputEventListeners(newLiElement);
        this.updateDuplicatedContentInNewLiElement(newLiElement);
        this.emailAddressInputList.appendChild(newLiElement);
        this.disableFirstRemoveEmailInputButtonIfOnlyOne();
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallyAdded"));
        window.dispatchEvent(new CustomEvent("newOnBlurValidationFieldsAdded", {
            detail: Array.from(newLiElement.querySelectorAll("input")).map(input => input.id),
        }));
    }

    exportEmailAddressesToJsonOutputElement() {
        const emailAddresses = Array.from(document.querySelectorAll(this.emailAddressInputSelector))
                                .map(input => input.value)
                                .filter(value => value.trim());
        this.emailAddressesJsonOutputElement.value = JSON.stringify(emailAddresses);
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    }

    loadPreviousData() {
        const previousData = JSON.parse(this.emailAddressesJsonOutputElement.value);
        if (!previousData) {
            return;
        }
        previousData.forEach((emailAddress, i) => {
            if (i !== 0) {
                this.addEmailAddressInput();
            }
            const correspondingLiElement = this.emailAddressInputList.querySelector(`li:nth-of-type(${i + 1})`);

            // Load email address
            const emailInput = correspondingLiElement.querySelector(this.emailAddressInputSelector);
            emailInput.value = emailAddress;
        });
    }
}


// Event listeners
window.addEventListener("load", () => {

    // Initialise multiple email address inputs
    const emailAddressSection = new EmailAddressContactInfoSection();
    emailAddressSection.setup();
});