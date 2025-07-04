import {
    cleanLocalId,
} from "/static/metadata_editor/components/localid_generation.js";
import {
    validateLocalIdAndProcessResults,
} from "/static/metadata_editor/components/localid_validation.js";
import {
    OrganisationEditor,
} from "/static/metadata_editor/organisation_editor.js";


class NewOrganisationEditor extends OrganisationEditor {
    setup() {
        super.setup();
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
            this.validateOrganisationLocalIdAndProcessResults();
        });
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
        await validateLocalIdAndProcessResults(this.localIdBase, this.localIdSuffix);
    }
}


window.addEventListener("load", async () => {
    const editor = new NewOrganisationEditor();
    if (editor.shortNameInput.value !== "") {
        editor.generateLocalIdAndUpdateLocalIdSuffixInputValue();
        await editor.validateOrganisationLocalIdAndProcessResults();
    }
});