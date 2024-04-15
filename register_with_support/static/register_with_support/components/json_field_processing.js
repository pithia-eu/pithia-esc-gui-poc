export function prepareKeywordsJSON() {
    const keywordObjects = [];
    const keywordsTableRows = document.querySelectorAll("#table-project-keywords tbody tr");
    keywordsTableRows.forEach(row => {
        const keywordTypeInput = row.querySelector("input[name='keyword_type']");
        const keywordTypeCodeInput = row.querySelector("input[name='keyword_type_code']");
        const keywordMultipleChoiceSelect = row.querySelector("select[name='keyword']");
        const selectedKeywordOptions = Array.from(keywordMultipleChoiceSelect.selectedOptions);
        keywordObjects.push({
            keywords: selectedKeywordOptions.map(option => option.value),
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
        const relatedPartyMultipleChoiceSelect = row.querySelector("select[name='related_party']");
        const relatedPartySelectedOptions = Array.from(relatedPartyMultipleChoiceSelect.selectedOptions);
        relatedPartyObjects.push({
            role: relatedPartyRoleSelect.value,
            parties: relatedPartySelectedOptions.map(option => option.value),
        });
    });
    const relatedPartiesHiddenInput = document.querySelector("input[name='related_parties_json']");
    relatedPartiesHiddenInput.value = JSON.stringify(relatedPartyObjects);
}

export function prepareStandardIdentifiersJSON() {
    const standardIdentifierObjects = [];
    const standardIdentifiersTableRows = document.querySelectorAll("#table-standard-identifiers tbody tr");
    standardIdentifiersTableRows.forEach(row => {
        const standardIdentifierAuthorityInput = row.querySelector("input[name='standard_identifier_authority']");
        const standardIdentifierValueInput = row.querySelector("input[name='standard_identifier']");
        standardIdentifierObjects.push({
            authority: standardIdentifierAuthorityInput.value,
            value: standardIdentifierValueInput.value,
        });
    });
    const standardIdentifiersHiddenInput = document.querySelector("input[name='standard_identifiers_json']");
    standardIdentifiersHiddenInput.value = JSON.stringify(standardIdentifierObjects);
}