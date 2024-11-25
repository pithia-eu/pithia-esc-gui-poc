const expandDescriptionButtons = document.querySelectorAll(".btn-expand-resource-description");
const expandDescriptionButtonDefaultTexts = Array.from(expandDescriptionButtons).reduce((acc, btn) => {
    acc[btn.dataset.target] = btn.textContent;
    return acc;
}, {});


// Credit for overflow detection: https://stackoverflow.com/a/67455839.
const isTextClamped = el => el.scrollHeight > el.clientHeight;

function setupExpandDescriptionButton(expandDescriptionButton) {
    const descriptionWrapperElement = document.querySelector(`#${expandDescriptionButton.dataset.target}`);
    if (!descriptionWrapperElement) {
        return;
    }
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
            expandDescriptionButton.innerText = expandDescriptionButtonDefaultTexts[expandDescriptionButton.dataset.target];
            return;
        }
        expandDescriptionButton.classList.add("expanded");
        descriptionWrapperElement.classList.add("expanded");
        expandDescriptionButton.innerText = "Show less";
    });
}

function enablePopovers() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl, {trigger: 'hover focus'}));
}

window.addEventListener("load", () => {
    enablePopovers();

    if (!expandDescriptionButtons) {
        return;
    }
    for (const expandDescriptionButton of expandDescriptionButtons) {
        setupExpandDescriptionButton(expandDescriptionButton);
    }
});