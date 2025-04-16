const searchInput = document.querySelector("#resource-name-search");
const categorySections = Array.from(document.querySelectorAll(".category-section"));
const linksByCategorySection = categorySections.reduce((accumulator, section) => {
    accumulator[section.id] = Array.from(section.querySelectorAll("a"));
    return accumulator;
}, {});


function searchCategorySection(input) {
    const inputLowerCase = input.toLowerCase();
    for (const sectionId in linksByCategorySection) {
        const section = document.querySelector(`#${sectionId}`);
        if (input.trim() === "") {
            section.classList.remove("d-none");
            continue;
        }
        const sectionLinks = linksByCategorySection[sectionId];
        if (!sectionLinks.some(link => link.textContent.toLowerCase().includes(inputLowerCase))) {
            section.classList.add("d-none");
            continue;
        }
        section.classList.remove("d-none");
        sectionLinks.forEach(link => {
            if (link.textContent.toLowerCase().includes(inputLowerCase)) {
                return link.classList.remove("text-body-secondary");
            }
            return link.classList.add("text-body-secondary");
        });
    }
}

searchInput.addEventListener("input", () => {
    searchCategorySection(searchInput.value);
});