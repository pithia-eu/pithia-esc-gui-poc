const listGroupContainers = document.querySelectorAll(".list-group-container");
const listGroupScrollContainers = document.querySelectorAll(".list-group-scroll-container");

function setFade(event) {
    window.requestAnimationFrame(function() {
        console.log('test');
        if (event.target.scrollHeight - event.target.scrollTop > event.target.clientHeight) {
            event.target.parentElement.classList.add('off-bottom');
        } else {
            event.target.parentElement.classList.remove('off-bottom');
        }
    });
}

listGroupScrollContainers.forEach(scrollContainer => {
    if (scrollContainer.scrollHeight === scrollContainer.clientHeight) {
        return scrollContainer.parentElement.classList.remove("off-bottom");
    }
    scrollContainer.addEventListener("scroll", setFade);
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