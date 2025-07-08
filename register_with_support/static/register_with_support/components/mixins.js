import {
    generateLocalId,
} from "/static/metadata_editor/components/localid_generation.js";
import {
    checkLocalIdIsUnique,
} from "/static/metadata_editor/components/localid_validation.js";


export const NewRegistrationEditorMixin = (Base) => class extends Base {
    constructor() {
        super();
        this.invalidFeedbackElement = document.querySelector(".local-id-input-group .invalid-feedback");
        this.nameInput = document.querySelector("input[name='name']");
        this.organisationInput = document.querySelector("select[name='organisation']");
        this.localIdInputGroup = document.querySelector(".local-id-input-group");
        this.localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
        this.namespacesByOrganisation = JSON.parse(document.getElementById("namespaces-by-organisation").textContent);
        this.namespaceInput = document.querySelector("input[name='namespace']");
        this.localIdSuffixInput = document.querySelector("input[name='localid']");
    }

    setupLocalIdAndNamespaceRelatedEventListeners() {
        this.nameInput.addEventListener("input", async () => {
            this.#generateValidLocalIdSuffixAndDisplayResults();
        });
        
        this.organisationInput.addEventListener("input", () => {
            const organisationUrl = this.organisationInput.value;
            if (organisationUrl === "") {
                return this.namespaceInput.value = "";
            }
            if (organisationUrl === "pithia") {
                this.namespaceInput.value = "pithia";
                return window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
            }
            this.namespaceInput.value = this.namespacesByOrganisation[organisationUrl].toLowerCase().replace(/\s/g, "");
            return window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
        });
    }

    async validateLocalIdAfterInitialEditorSetupIfNeeded() {
        if (this.nameInput.value !== "") {
            await this.#generateValidLocalIdSuffixAndDisplayResults();
        }
    }

    async validateLocalIdAndProcessResults(localIdSuffix) {
        const localIdCheck = await checkLocalIdIsUnique(this.localIdBase + "_" + localIdSuffix);
        if ("error" in localIdCheck) {
            if ("displayError" in localIdCheck) this.#displayLocalIdError(localIdCheck.error);
            return;
        }
        const isLocalIdInUse = localIdCheck.result;

        if (isLocalIdInUse) {
            this.#displayLocalIdSuggestion(localIdCheck, localIdSuffix);
        } else {
            this.localIdSuffixInput.classList.remove("is-invalid");
        }
        window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
    }

    async #generateValidLocalIdSuffixAndDisplayResults() {
        const localIdSuffix = generateLocalId(this.nameInput.value);
        this.localIdSuffixInput.value = localIdSuffix;

        await this.validateLocalIdAndProcessResults(localIdSuffix);
    }

    #displayLocalIdError(error) {
        this.localIdInputGroup.classList.add("was-validated");
        this.localIdSuffixInput.classList.add("is-invalid");
        this.invalidFeedbackElement.textContent = error;
    }

    #displayLocalIdSuggestion(localIdCheck, localIdSuffix) {
        if (!("suggestion" in localIdCheck)) {
            return this.#displayLocalIdError(`Local ID with suffix "${localIdSuffix}" has been taken. An alternative cannot be suggested at this time. Please try generating another local ID.`);
        }
        const suggestionSuffix = localIdCheck.suggestion.split("_").slice(1).join("_");
        this.localIdSuffixInput.value = suggestionSuffix;
        return this.#displayLocalIdError(`Local ID with suffix "${localIdSuffix}" is already in use so "${suggestionSuffix}" will be used instead.`);
    }
}