export function prepareRelatedPartiesJSON() {
    const relatedPartiesCategorised = {};
    const relatedPartyTableRows = document.querySelectorAll("#table-related-parties tbody tr");
    relatedPartyTableRows.forEach(row => {
        const relatedPartyRoleSelect = row.querySelector("select[name='related_party_role']");
        if (relatedPartyRoleSelect !== null && relatedPartyRoleSelect.value.trim() !== "") {
            const relatedPartySelects = Array.from(row.querySelectorAll("select[name='related_party']"));
            relatedPartiesCategorised[relatedPartyRoleSelect.value] = relatedPartySelects.map(select => select.value);
        }
    });
    const relatedPartiesHiddenInput = document.querySelector("input[name='related_parties_json']");
    relatedPartiesHiddenInput.value = JSON.stringify(relatedPartiesCategorised);
}