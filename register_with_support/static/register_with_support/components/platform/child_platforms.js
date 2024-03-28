import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

const addChildPlatformButton = editorForm.querySelector("#add-cp-button");
const childPlatformsList = editorForm.querySelector("#list-child-platforms");

function getLiElementByChildNode(childNode) {
    const childPlatformListItems = childPlatformsList.querySelectorAll("li");
    for (const listItem of childPlatformListItems) {
        if (listItem.contains(childNode)) {
            return listItem;
        }
    }
}

function getRemainingChildPlatformsInList() {
    return childPlatformsList.querySelectorAll("li").length;
}

function removeChildPlatform(event) {
    const removeChildPlatformButton = event.currentTarget;
    const containingLiElement = getLiElementByChildNode(removeChildPlatformButton);
    childPlatformsList.removeChild(containingLiElement);
    if (getRemainingChildPlatformsInList() === 1) {
        const firstRemoveChildPlatformButton = childPlatformsList.querySelector("li .remove-cp-button");
        firstRemoveChildPlatformButton.disabled = true;
    }
}

function setupRemoveChildPlatformButton(removeChildPlatformButton) {
    removeChildPlatformButton.addEventListener("click", removeChildPlatform);
}

function addChildPlatform() {
    const newLiElement = document.createElement("LI");
    const firstCpLiElement = childPlatformsList.querySelector("li:first-of-type");
    newLiElement.classList = firstCpLiElement.classList;
    newLiElement.outerHTML = firstCpLiElement.outerHTML;
    newLiElement.innerHTML = firstCpLiElement.innerHTML;
    const removeChildPlatformButton = newLiElement.querySelector(".remove-cp-button");
    removeChildPlatformButton.disabled = false;
    setupRemoveChildPlatformButton(removeChildPlatformButton);
    childPlatformsList.appendChild(newLiElement);
    if (getRemainingChildPlatformsInList() > 1) {
        const firstRemoveChildPlatformButton = childPlatformsList.querySelector("li .remove-cp-button");
        firstRemoveChildPlatformButton.disabled = false;
    }
}

function setupAddChildPlatformButton() {
    addChildPlatformButton.addEventListener("click", addChildPlatform);
}

export function setupChildPlatformsList() {
    const removeChildPlatformButtons = editorForm.querySelectorAll(".remove-cp-button");
    removeChildPlatformButtons.forEach(btn => {
        setupRemoveChildPlatformButton(btn);
    });
    if (removeChildPlatformButtons.length === 1) {
        removeChildPlatformButtons[0].disabled = true;
    }
    setupAddChildPlatformButton();
}