window.addEventListener("DOMContentLoaded", () => {
    const serviceFunctionLists = document.querySelectorAll(".service-function-list");
    if (!serviceFunctionLists) return;
    serviceFunctionLists.forEach(serviceFunctionList => {
        const showAllButton = document.querySelector(`.show-all-btn[data-for="${serviceFunctionList.id}"]`);
        if (!showAllButton) return;
        const defaultButtonContent = showAllButton.textContent;
        showAllButton.addEventListener("click", () => {
            if (serviceFunctionList.classList.contains("show-all")) {
                serviceFunctionList.classList.remove("show-all");
                return showAllButton.textContent = defaultButtonContent;
            }
            serviceFunctionList.classList.add("show-all");
            return showAllButton.textContent = "Hide other service functions";
        });
    });
});