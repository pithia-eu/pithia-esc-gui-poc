function setupDeleteSubmitButton() {
    const deleteSubmitButton = document.querySelector('button[type="submit"]')
    deleteSubmitButton.disabled = true;

    const resourceName = JSON.parse(document.getElementById("resource-name").textContent);
    const confirmResourceName = document.getElementById("confirm-resource-name");
    confirmResourceName.addEventListener("input", event => {
        if (confirmResourceName.value === resourceName) {
            return deleteSubmitButton.disabled = false;
        }
        return deleteSubmitButton.disabled = true;
    });
}

window.onload = setupDeleteSubmitButton;