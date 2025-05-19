document.getElementById("ontology-search-form").addEventListener("submit", event => {
    const checkedCheckboxes = document.querySelectorAll("#ontology-search-form input[type=checkbox].search-term-checkbox:checked:not(:disabled, [name=phenomenon], [name=measurand])");
    if (checkedCheckboxes.length === 0) {
        event.preventDefault();
        return alert('Select at least one Feature of Interest, Computation Type, Instrument Type, Annotation Type or Observed Property.');
    }
});