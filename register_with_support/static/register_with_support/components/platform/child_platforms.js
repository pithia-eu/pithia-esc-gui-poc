import {
    editorForm,
} from "/static/register_with_support/components/base_editor.js";

const addChildPlatformButton = editorForm.querySelector("#add-cp-button");
const childPlatformsList = editorForm.querySelector("#list-child-platforms");

function removeChildPlatform() {

}

function setupRemoveChildPlatformButton(removeChildPlatformButton) {
    removeChildPlatformButton.addEventListener("click", removeChildPlatformButton);
}

function addChildPlatform() {
    const newLiElement = document.createElement("LI");
    const firstCpLiElement = childPlatformsList.querySelector("li:first-of-type");
    newLiElement.classList = firstCpLiElement.classList;
    newLiElement.outerHTML = firstCpLiElement.outerHTML;
    newLiElement.innerHTML = firstCpLiElement.innerHTML;
    const removeChildPlatformButton = newLiElement.querySelector(".remove-cp-button");
    setupRemoveChildPlatformButton(removeChildPlatformButton);
    childPlatformsList.appendChild(newLiElement);
}

function setupAddChildPlatformButton() {
    addChildPlatformButton.addEventListener("click", addChildPlatform);
}

export function setupChildPlatformsList() {
    const removeChildPlatformButtons = editorForm.querySelectorAll(".remove-cp-button");
    removeChildPlatformButtons.forEach(btn => {
        setupRemoveChildPlatformButton(btn);
    });
    setupAddChildPlatformButton();
}