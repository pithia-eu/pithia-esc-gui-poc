Array.from(document.getElementsByClassName("delete-form")).forEach(form => {
    form.addEventListener("submit", event => {
        if (!confirm("Are you sure you want to delete this resource?")) {
            event.preventDefault();
            return false;
        }
        return true;
    });
});