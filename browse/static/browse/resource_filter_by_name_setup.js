function updateResourceCount(resourceCountElement, numResourceCount, typeReadable, typePluralReadable, reset = false) {
    const resourceCountText = `${numResourceCount} ${(numResourceCount === 1) ? typeReadable : typePluralReadable}`;
    if (reset) {
        return resourceCountElement.textContent = resourceCountText;
    }
    return resourceCountElement.textContent = `Found ${resourceCountText}`;
}

export function filterResourceList(
    searchInput,
    searchableList,
    searchableListClone,
    searchableListItemText,
    resourceCountElement,
    typeReadable,
    typePluralReadable) {
    const searchInputValue = searchInput.value.trim();
    if (!searchInputValue) {
        updateResourceCount(resourceCountElement, searchableListClone.childElementCount, typeReadable, typePluralReadable, true);
        return searchableList.replaceChildren(...searchableListClone.cloneNode(true).children);
    }
    const searchInputValueSplit = searchInputValue.split(/\s/);
    const fragment = new DocumentFragment();
    for (const property in searchableListItemText) {
        const listItemText = searchableListItemText[property];
        if (!searchInputValueSplit.every((searchInputValuePart) => listItemText.toLowerCase().includes(searchInputValuePart.toLowerCase()))) {
            continue;
        }
        const listItem = searchableListClone.querySelector(`#${property}`);
        try {
            fragment.append(listItem.cloneNode(true));
        } catch (error) {
            console.error(error);
        }
    }
    updateResourceCount(resourceCountElement, fragment.childElementCount, typeReadable, typePluralReadable, true);
    return searchableList.replaceChildren(fragment);
}