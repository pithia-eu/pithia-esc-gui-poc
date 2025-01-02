const onlineResourceFileListWrapper = document.querySelector(".online-resource-files-list-wrapper");
const onlineResourceFileList = document.querySelector(".online-resource-files-list");
const sourceFileListItemTemplate = JSON.parse(document.querySelector("#source-file-list-item-template").textContent);

const onlineResourceFileInputSwitch = document.querySelector("input[name='is_file_uploaded_for_each_online_resource']");

const emptyOnlineResourceFileListItem = document.createElement("LI");
emptyOnlineResourceFileListItem.className = "list-group-item list-group-item-light";
emptyOnlineResourceFileListItem.textContent = "This Catalogue Data Subset has no online resources.";
const UNIX_TIMESTAMP_LENGTH = Date.now().toString().length;


export function addTimestampToElementId(elementId) {
    const isTimestampAddedAlready = Number.isInteger(Number.parseInt(elementId.slice(-UNIX_TIMESTAMP_LENGTH)));
    if (isTimestampAddedAlready) {
        return `${elementId.slice(0, -UNIX_TIMESTAMP_LENGTH)}${Date.now()}`
    }
    return `${elementId}${Date.now()}`;
}

function updateElementsWithDuplicatedIdsForOnlineResourceFileListItem(elementsWithDuplicatedIds, onlineResourceFileListItem) {
    for (const element of elementsWithDuplicatedIds) {
        const newId = addTimestampToElementId(element.id);
        const correspondingLabels = onlineResourceFileListItem.querySelectorAll(`label[for="${element.id}"]`);
        const correspondingAriaDescBys = onlineResourceFileListItem.querySelectorAll(`[aria-describedby="${element.id}"]`);
        element.id = newId;
        correspondingLabels.forEach(label => {
            label.htmlFor = newId;
        });
        correspondingAriaDescBys.forEach(element => {
            element.setAttribute("aria-describedby", newId);
        });
    }
}

function updateFileInputAndLabelForOnlineResource(fileInput, fileInputLabel, onlineResourceName) {
    fileInput.name = fileInput.name + "__" + onlineResourceName;
    fileInputLabel.textContent = `File for ${onlineResourceName}`;
}

function toggleOnlineResourceListVisibility(isVisible) {
    if (isVisible) {
        return onlineResourceFileListWrapper.classList.remove("disabled");
    }
    onlineResourceFileListWrapper.classList.add("disabled");
}

export function clearOnlineResourceList() {
    onlineResourceFileList.replaceChildren();
}

export function setupOnlineResourceFilesListToggle() {
    toggleOnlineResourceListVisibility(onlineResourceFileInputSwitch.checked);
}

export function loadOnlineResourceFiles(metadataFileXmlString) {
    const parser = new DOMParser();
    const metadataDoc = parser.parseFromString(metadataFileXmlString, "application/xml");
    const onlineResources = metadataDoc.querySelectorAll(":scope > source > OnlineResource");
    if (!onlineResources.length) {
        clearOnlineResourceList();
        return;
    }

    // Load a list of the data subset's
    // online resources to allow the user
    // to upload a file for each resource.
    const onlineResourceFileListItems = [];
    for (const onlineResource of onlineResources) {
        const onlineResourceFileListItem = document.createRange().createContextualFragment(sourceFileListItemTemplate);
        const onlineResourceName = onlineResource.querySelector("name").textContent;
        
        // Set online source name
        const listItemSourceName = onlineResourceFileListItem.querySelector(".source-name");
        listItemSourceName.textContent = onlineResourceName;

        // Update any element IDs to be unique,
        // and update any corresponding labels.
        const elementsWithIds = onlineResourceFileListItem.querySelectorAll("[id]");
        updateElementsWithDuplicatedIdsForOnlineResourceFileListItem(elementsWithIds, onlineResourceFileListItem);

        // Update file inputs and labels
        const onlineResourceFileInput = onlineResourceFileListItem.querySelector("input[type='file']");
        const onlineResourceFileInputLabel = onlineResourceFileListItem.querySelector(`label[for="${onlineResourceFileInput.id}"]`);
        updateFileInputAndLabelForOnlineResource(
            onlineResourceFileInput,
            onlineResourceFileInputLabel,
            onlineResourceName
        );

        onlineResourceFileListItems.push(onlineResourceFileListItem);
    }
    onlineResourceFileList.replaceChildren(...onlineResourceFileListItems);

    const onlineResourceFilesInputs = Array.from(document.querySelectorAll("input[name='additional_online_resource_file']"));
    const onlineResourceFiles = onlineResourceFilesInputs.map(input => input.value);
}

onlineResourceFileInputSwitch.addEventListener("change", () => {
    toggleOnlineResourceListVisibility(onlineResourceFileInputSwitch.checked);
});