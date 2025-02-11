const permissionShortcutLinks = Array.from(document.querySelectorAll("a[href^='#permission_']"));

for (const link of permissionShortcutLinks) {
    link.addEventListener("click", () => {
        const detailsElementId = link.href.split("/").pop();
        const detailsElement = document.querySelector(detailsElementId);
        detailsElement.open = true;
    });
}