export function loadTableOfContents() {
    const tableOfContents = document.querySelector("#toc");
    const h2Elements = document.querySelectorAll(".resource-detail-section h2:not(.exclude-from-toc)");

    h2Elements.forEach(h2Element => {
        // Configure link to <h2> element
        const anchorElement = document.createElement("A");
        anchorElement.setAttribute("href", "#");
        if (h2Element.hasAttribute("id")) {
            anchorElement.setAttribute("href", `#${h2Element.id}`);
        }
        anchorElement.textContent = h2Element.textContent.trim();
        anchorElement.classList.add("fs-6");
        anchorElement.classList.add("px-0");
        anchorElement.classList.add("link-plain-by-default");
        anchorElement.classList.add("list-group-item");
        anchorElement.classList.add("list-group-item-action");
        // Add link to TOC
        tableOfContents.appendChild(anchorElement);
    });
}
