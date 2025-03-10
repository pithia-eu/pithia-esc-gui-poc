const COPY_BUTTON_TOOLTIP_DEFAULT_TEXT = 'Copy Ontology IRI';
const COPY_BUTTON_TOOLTIP_COPIED_TEXT = 'Copied!';
let ontologyIriCopyButtonTimeout;


export async function setupOntologyIriCopyButtons() {
    const ontologyIriCopyButtons = document.querySelectorAll('.btn-copy-ontology-iri');
    for await (const button of ontologyIriCopyButtons) {
        const tooltip = new bootstrap.Tooltip(button, {});
        button.addEventListener('hidden.bs.tooltip', () => {
            tooltip.setContent({
                '.tooltip-inner': COPY_BUTTON_TOOLTIP_DEFAULT_TEXT
            });
        });
        button.addEventListener("click", async () => {
            const ontologyIri = button.dataset.ontologyIri;
            await navigator.clipboard.writeText(ontologyIri);
            if (ontologyIriCopyButtonTimeout) {
                window.clearTimeout(ontologyIriCopyButtonTimeout);
            }
            ontologyIriCopyButtonTimeout = window.setTimeout(() => {
                tooltip.setContent({
                    '.tooltip-inner': COPY_BUTTON_TOOLTIP_DEFAULT_TEXT
                });
            }, 1500);
            tooltip.setContent({
                '.tooltip-inner': COPY_BUTTON_TOOLTIP_COPIED_TEXT
            });
        });
    }
}