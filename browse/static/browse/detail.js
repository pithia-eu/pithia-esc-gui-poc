const descriptionElement = document.querySelector(".resource-description");
const expandDescriptionButton = document.querySelector(".btn-expand-resource-description");


// Credit for overflow detection: https://stackoverflow.com/a/67455839.
const isTextClamped = el => el.scrollHeight > el.clientHeight;
new ResizeObserver(e => {
    if (descriptionElement.classList.contains("expanded")) {
        return expandDescriptionButton.classList.remove("hidden");
    }

    if (isTextClamped(e[0].target)) {
        return expandDescriptionButton.classList.remove("hidden");
    }
    return expandDescriptionButton.classList.add("hidden");
}).observe(descriptionElement);

expandDescriptionButton.addEventListener("click", () => {
    if (expandDescriptionButton.classList.contains("expanded")) {
        expandDescriptionButton.classList.remove("expanded");
        descriptionElement.classList.remove("expanded");
        expandDescriptionButton.innerText = "Show more";
        return;
    }
    expandDescriptionButton.classList.add("expanded");
    descriptionElement.classList.add("expanded");
    expandDescriptionButton.innerText = "Show less";
});