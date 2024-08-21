const descriptionWrapperElement = document.querySelector(".resource-description-wrapper");
const expandDescriptionButton = document.querySelector(".btn-expand-resource-description");

function setupExpandDescriptionButton() {
    // Credit for overflow detection: https://stackoverflow.com/a/67455839.
    const isTextClamped = el => el.scrollHeight > el.clientHeight;
    new ResizeObserver(e => {
        if (descriptionWrapperElement.classList.contains("expanded")) {
            return expandDescriptionButton.classList.remove("hidden");
        }
        
        if (isTextClamped(e[0].target)) {
            return expandDescriptionButton.classList.remove("hidden");
        }
        return expandDescriptionButton.classList.add("hidden");
    }).observe(descriptionWrapperElement);
    
    expandDescriptionButton.addEventListener("click", () => {
        if (expandDescriptionButton.classList.contains("expanded")) {
            expandDescriptionButton.classList.remove("expanded");
            descriptionWrapperElement.classList.remove("expanded");
            expandDescriptionButton.innerText = "Show more";
            return;
        }
        expandDescriptionButton.classList.add("expanded");
        descriptionWrapperElement.classList.add("expanded");
        expandDescriptionButton.innerText = "Show less";
    });
}

window.addEventListener("load", () => {
    if (!descriptionWrapperElement) {
        return;
    }
    setupExpandDescriptionButton();
});