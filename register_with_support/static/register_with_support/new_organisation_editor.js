import {
    cleanLocalId,
} from "/static/metadata_editor/components/localid_generation.js";
import {
    OrganisationEditor,
} from "/static/metadata_editor/organisation_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";
import {
    NewRegistrationEditorMixin,
} from "/static/register_with_support/components/mixins.js";


class NewOrganisationEditor extends NewRegistrationEditorMixin(OrganisationEditor) {
    setupClassVariables() {
        super.setupClassVariables();
        this.shortNameInput = document.querySelector("input[name='short_name']");
        this.localIdBase = JSON.parse(document.getElementById("local-id-base").textContent);
        this.localIdSuffixInput = document.querySelector("input[name='localid']");
        this.localIdSuffix = undefined;
    }

    setupEventListeners() {
        super.setupEventListeners();

        this.shortNameInput.addEventListener("input", async () => {
            this.generateLocalIdAndUpdateLocalIdSuffixInputValue();
            window.dispatchEvent(new CustomEvent("wizardFieldProgrammaticallySet"));
            await this.validateOrganisationLocalIdAndProcessResults();
        });
    }

    async runAfterInitialEditorSetup() {
        if (this.shortNameInput.value !== "") {
            this.generateLocalIdAndUpdateLocalIdSuffixInputValue();
            await this.validateOrganisationLocalIdAndProcessResults();
        }
    }

    generateLocalId(shortName) {
        // Organisation local ID is generated using a different method
        // to all other metadata types.
        return cleanLocalId(shortName.toUpperCase().replace(/\s/g, ""));
    }

    generateLocalIdAndUpdateLocalIdSuffixInputValue() {
        this.localIdSuffix = this.generateLocalId(this.shortNameInput.value);
        this.localIdSuffixInput.value = this.localIdSuffix;
    }

    async validateOrganisationLocalIdAndProcessResults() {
        await this.validateLocalIdAndProcessResults(this.localIdSuffix);
    }
}


window.addEventListener("load", async () => {
    const editor = await setupEditor(NewOrganisationEditor);
});