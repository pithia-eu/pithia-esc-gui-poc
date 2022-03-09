const ontologyTreeLiElems = document.querySelectorAll("li");
ontologyTreeLiElems.forEach(li => {
    const childDetailsElems = li.querySelectorAll("details");
    const firstChildCheckbox = li.querySelector("input[type='checkbox']");
    firstChildCheckbox.addEventListener("change", event => {
        childDetailsElems.forEach(details => {
            details.open = true;
        });
        const otherChildCheckboxes = li.querySelectorAll("input[type='checkbox']");
        otherChildCheckboxes.forEach(childCheckbox => {
            childCheckbox.checked = firstChildCheckbox.checked;
        });
    });
});