const simpleSearchForm = document.querySelector("#simple-search-form");
const simpleSearchFormSubmitButton = document.querySelector("#simple-search-form button[type='submit']");

simpleSearchForm.addEventListener("submit", event => {
    simpleSearchFormSubmitButton.innerHTML = `<div class="spinner-border spinner-border-sm text-light mx-3" role="status">
                                                <span class="visually-hidden">Loading...</span>
                                            </div>`;
});