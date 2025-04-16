const searchInput = document.querySelector("#resource-name-search");
const categorySections = Array.from(document.querySelectorAll(".category-section"));
const listItemsByCategorySection = categorySections.reduce((accumulator, section) => {
    accumulator[section.id] = Array.from(section.querySelectorAll("li"));
    return accumulator;
}, {});


function searchCategorySection(input) {
    const inputLowerCase = input.toLowerCase();
    for (const sectionId in listItemsByCategorySection) {
        const section = document.querySelector(`#${sectionId}`);
        const sectionListItems = listItemsByCategorySection[sectionId];
        if (input.trim() === "") {
            section.classList.remove("d-none");
            sectionListItems.forEach(link => {
                link.classList.remove("fw-semibold");
                return link.classList.remove("d-none");
            });
            continue;
        }
        if (!sectionListItems.some(link => link.textContent.toLowerCase().includes(inputLowerCase))) {
            section.classList.add("d-none");
            continue;
        }
        section.classList.remove("d-none");
        sectionListItems.forEach(link => {
            if (link.textContent.toLowerCase().includes(inputLowerCase)) {
                link.classList.add("fw-semibold");
                return link.classList.remove("d-none");
            }
            link.classList.remove("fw-semibold");
            return link.classList.add("d-none");
        });
    }
}

searchInput.addEventListener("input", () => {
    searchCategorySection(searchInput.value);
});