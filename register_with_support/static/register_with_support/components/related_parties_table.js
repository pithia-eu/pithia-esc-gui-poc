import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";
import {
    checkAndConfigureRequiredAttributesOfSelects,
} from "/static/register_with_support/components/conditional_required_fields.js";
import {
    DynamicEditorTable,
} from "/static/register_with_support/components/table_utils.js";


class RelatedPartiesTable extends DynamicEditorTable {
    constructor() {
        super(
            "#table-related-parties",
            "#table-related-parties tbody",
            "#add-rprrow-button",
            ".remove-rprrow-button",
            "#related-parties-row-content-template",
            "input[name='related_parties_json']"
        );
    }

    exportTableData() {
        const relatedPartyObjects = [];
        this.rows.forEach(row => {
            const relatedPartyRoleSelect = row.querySelector("select[name='related_party_role']");
            const relatedPartyMultipleChoiceSelect = row.querySelector("select[name='related_party']");
            const relatedPartySelectedOptions = Array.from(relatedPartyMultipleChoiceSelect.selectedOptions);
            relatedPartyObjects.push({
                role: relatedPartyRoleSelect.value,
                parties: relatedPartySelectedOptions.map(option => option.value),
            });
        });
        return relatedPartyObjects;
    }

    setupDuplicatedContentInNewRow(newRow) {
        super.setupDuplicatedContentInNewRow(newRow);

        // Reset any selected choices
        const newRowSelects = newRow.querySelectorAll("select");
        newRowSelects.forEach(select => {
            select.querySelectorAll("option[selected]").forEach(option => {
                option.selected = false;
            });
            select.className = "form-select";
            select.removeAttribute("required");
        });
    }

    addRow() {
        const newRow = super.addRow();

        window.dispatchEvent(new CustomEvent("newSelectsAdded", {
            detail: Array.from(newRow.querySelectorAll("select:not([multiple])")).map(select => select.id),
        }));
        window.dispatchEvent(new CustomEvent("newMultipleChoiceSelectsAdded", {
            detail: Array.from(newRow.querySelectorAll("select[multiple]")).map(select => select.id),
        }));
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);

        const selects = Array.from(newRow.querySelectorAll("select"));
        selects.forEach(s => {
            s.addEventListener("change", e => {
                checkAndConfigureRequiredAttributesOfSelects(selects);
                this.exportTableDataToJsonAndStoreInOutputElement();
            });
        });
    }

    loadPreviousData() {
        const previousData = JSON.parse(editorForm.querySelector("input[name='related_parties_json']").value);
        if (!previousData) {
            return;
        }
        previousData.forEach((relatedPartyObject, i) => {
            if (i !== 0) {
                this.addRow();
            }
            const role = relatedPartyObject.role;
            const parties = relatedPartyObject.parties;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);

            // Load role
            const roleSelect = correspondingRow.querySelector("select[name='related_party_role']");
            roleSelect.value = role;
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: roleSelect.id,
            }));

            // Load parties
            const partySelect = correspondingRow.querySelector("select[name='related_party']");
            partySelect.value = "";
            parties.forEach(party => {
                partySelect.querySelector(`option[value="${party}"]`).selected = true;
            });
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: partySelect.id,
            }));

            checkAndConfigureRequiredAttributesOfSelects(Array.from(correspondingRow.querySelectorAll("select")));
        });
    }
}

export function setupRelatedPartiesTable() {
    const newRelatedPartiesTable = new RelatedPartiesTable();
    newRelatedPartiesTable.setup();
    return newRelatedPartiesTable;
}