export function checkAndConfigureRequiredAttributesOfSelects(selects) {
    if (!selects) {
        return;
    }
    const isRequired = !(selects.every(s => s.value === "")) || selects.every(s => s.value !== "");
    for (const s of selects) {
        if (!isRequired) {
            s.removeAttribute("required");
            continue;
        }
        s.setAttribute("required", true);
        if (s.value === "") {
            s.value = null;
        }
    }
}