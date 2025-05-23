const COPY_BUTTON_TOOLTIP_COPIED_TEXT = 'Copied IRI';
const ontologyIriCopyButtonTimeouts = {};


export async function setupOntologyIriCopyButtons() {
    const ontologyIriCopyButtons = document.querySelectorAll('.btn-copy-ontology-iri');
    for await (const button of ontologyIriCopyButtons) {
        const buttonSpan = button.querySelector("span");
        const buttonDefaultText = buttonSpan.textContent;
        button.addEventListener("click", async () => {
            const ontologyIri = button.dataset.ontologyIri;
            await navigator.clipboard.writeText(ontologyIri);
            if (ontologyIri in ontologyIriCopyButtonTimeouts) {
                window.clearTimeout(ontologyIriCopyButtonTimeouts[ontologyIri]);
                delete ontologyIriCopyButtonTimeouts[ontologyIri];
            }
            ontologyIriCopyButtonTimeouts[ontologyIri] = window.setTimeout(() => {
                buttonSpan.textContent = buttonDefaultText;
                button.removeAttribute("disabled");
            }, 1500);
            buttonSpan.textContent = COPY_BUTTON_TOOLTIP_COPIED_TEXT;
            button.setAttribute("disabled", "true");
        });
    }
}