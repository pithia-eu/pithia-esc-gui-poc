const listGroupScrollContainers = document.querySelectorAll(".list-group-scroll-container");

function setFade(event) {
    window.requestAnimationFrame(function() {
        if (event.target.scrollHeight - event.target.scrollTop > event.target.clientHeight) {
            event.target.parentElement.classList.add('off-bottom');
        } else {
            event.target.parentElement.classList.remove('off-bottom');
        }
    });
}

function getContainingSectionOfNode(node) {
    const sections = document.querySelectorAll("section");
    for (const section of sections) {
        if (section.contains(node)) {
            return section;
        }
    }
}

export function disableScrollContainerForSection(section) {
    const scrollContainer = section.querySelector(".list-group-scroll-container");
    if (!scrollContainer) {
        return;
    }
    scrollContainer.parentElement.classList.remove("off-bottom");
    scrollContainer.classList.remove("default-view");
    const showAllDataCollectionsButton = section.querySelector(".show-all-dcs-button");
    if (!showAllDataCollectionsButton) {
        return;
    }
    return showAllDataCollectionsButton.parentElement.classList.add("d-none");
}

export function enableScrollContainerForSection(section) {
    const scrollContainer = section.querySelector(".list-group-scroll-container");
    if (!scrollContainer) {
        return;
    }
    window.setTimeout(() => {
        if (scrollContainer.scrollHeight !== scrollContainer.clientHeight) {
            scrollContainer.parentElement.classList.add("off-bottom");
        }
    }, 100);
    scrollContainer.classList.add("default-view");
    const showAllDataCollectionsButton = section.querySelector(".show-all-dcs-button");
    if (!showAllDataCollectionsButton) {
        return;
    }
    return showAllDataCollectionsButton.parentElement.classList.remove("d-none");
}

listGroupScrollContainers.forEach(scrollContainer => {
    if (scrollContainer.scrollHeight === scrollContainer.clientHeight) {
        scrollContainer.parentElement.classList.remove("off-bottom");
        const containingSection = getContainingSectionOfNode(scrollContainer);
        if (containingSection) {
            const showAllDCsButtonContainer = containingSection.querySelector(".show-all-dcs-button-container");
            if (!showAllDCsButtonContainer) {
                return;
            }
            containingSection.removeChild(showAllDCsButtonContainer);
        }
        return;
    }
    scrollContainer.addEventListener("scroll", setFade);
});

document.querySelectorAll(".show-all-dcs-button").forEach(btn => {
    btn.addEventListener("click", () => {
        const containingSection = getContainingSectionOfNode(btn);
        if (!containingSection) {
            return;
        }
        disableScrollContainerForSection(containingSection);
    });
});

document.querySelectorAll(".data-collection-category").forEach(summaryElem => {
    summaryElem.addEventListener("click", e => {
        if (window.matchMedia("(pointer: fine)").matches) {
            return e.preventDefault();
        }
    });
});

window.addEventListener("load", () => {
    if (window.matchMedia("(pointer: coarse)").matches) {
        document.querySelectorAll(".data-collection-category").forEach(summaryElem => {
            summaryElem.removeAttribute("tabindex");
        });
    }
});