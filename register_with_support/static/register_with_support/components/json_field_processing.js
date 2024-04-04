export function prepareKeywordsJSON() {
    const keywordObjects = [];
    const keywordsTableRows = document.querySelectorAll("#table-project-keywords tbody tr");
    keywordsTableRows.forEach(row => {
        const keywordTypeInput = row.querySelector("input[name='keyword_type']");
        const keywordTypeCodeInput = row.querySelector("input[name='keyword_type_code']");
        const keywordsForTypeInputs = Array.from(row.querySelectorAll("input[name='keyword']"));
        keywordObjects.push({
            keywords: keywordsForTypeInputs.map(keywordInput => keywordInput.value),
            type: {
                codeList: keywordTypeCodeInput.value,
                codeListValue: keywordTypeInput.value,
            }
        });
    });
    const keywordsHiddenInput = document.querySelector("input[name='keywords_json']");
    keywordsHiddenInput.value = JSON.stringify(keywordObjects);
}

export function prepareRelatedPartiesJSON() {
    const relatedPartyObjects = [];
    const relatedPartyTableRows = document.querySelectorAll("#table-related-parties tbody tr");
    relatedPartyTableRows.forEach(row => {
        const relatedPartyRoleSelect = row.querySelector("select[name='related_party_role']");
        const relatedPartySelects = Array.from(row.querySelectorAll("select[name='related_party']"));
        relatedPartyObjects.push({
            role: relatedPartyRoleSelect.value,
            parties: relatedPartySelects.map(select => select.value),
        });
    });
    const relatedPartiesHiddenInput = document.querySelector("input[name='related_parties_json']");
    relatedPartiesHiddenInput.value = JSON.stringify(relatedPartyObjects);
}