const shortNameInput = document.querySelector("input[name='short_name']");

shortNameInput.addEventListener("input", () => {
    const shortName = shortNameInput.value;
    const localIdInput = document.querySelector("input[name='local_id']");
    localIdInput.value = shortName.toUpperCase();
});