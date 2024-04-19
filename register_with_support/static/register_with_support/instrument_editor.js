const opModeIdDescriptionTextarea = document.querySelector("textarea[name='operational_mode_description']");

opModeIdDescriptionTextarea.addEventListener("focus", () => {
    opModeIdDescriptionTextarea.style.height = opModeIdDescriptionTextarea.scrollHeight + "px";
});

opModeIdDescriptionTextarea.addEventListener("input", () => {
    opModeIdDescriptionTextarea.style.height = opModeIdDescriptionTextarea.scrollHeight + "px";
});

opModeIdDescriptionTextarea.addEventListener("blur", () => {
    opModeIdDescriptionTextarea.removeAttribute("style");
});