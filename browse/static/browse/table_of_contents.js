const furtherInformationSectionDetailsElement = document.querySelector("#further-information-section > details");


function loadTableOfContentsElement(tableOfContentsElement) {
    // Clear placeholders
    tableOfContentsElement.innerHTML = "";

    // Add links to headings
    const tocHeadings = document.querySelectorAll(".resource-detail-section h2:not(.exclude-from-toc), .include-in-toc");

    tocHeadings.forEach(tocHeading => {
        const tocListItem = document.createElement("LI");
        tocListItem.classList.add("list-group-item");
        tocListItem.classList.add("p-0");
        // Configure link to heading
        const anchorElement = document.createElement("A");
        anchorElement.setAttribute("href", "#");
        if (tocHeading.hasAttribute("id")) {
            anchorElement.setAttribute("href", `#${tocHeading.id}`);
        }
        let h2TextContent = tocHeading.childNodes[0].textContent;
        if (!h2TextContent.trim()) {
            h2TextContent = tocHeading.textContent;
        }
        anchorElement.textContent = h2TextContent;
        anchorElement.classList.add("d-inline-block");
        anchorElement.classList.add("fs-6");
        anchorElement.classList.add("text-body");
        anchorElement.classList.add("link-plain-by-default");
        anchorElement.classList.add("list-group-item-action");
        anchorElement.classList.add("w-100");
        anchorElement.classList.add("px-3");
        anchorElement.classList.add("py-2");
        if (furtherInformationSectionDetailsElement.querySelector(`#${tocHeading.id}`)) {
            anchorElement.addEventListener("click", () => {
                furtherInformationSectionDetailsElement.setAttribute("open", "open");
            });
        }
        tocListItem.append(anchorElement);
        // Add link to TOC
        tableOfContentsElement.appendChild(tocListItem);
    });
}

export function loadTableOfContentsElements() {
    const tableOfContentsElements = document.querySelectorAll(".toc");
    for (const tableOfContentsElement of tableOfContentsElements) {
        try {
            loadTableOfContentsElement(tableOfContentsElement);
        } catch (error) {
            console.error("Encountered an error whilst loading table of contents.", error);
        };
    }
}
