import {
    checkForSimilarSourceNames,
} from "/static/validation/catalogue_data_subset_validation.js";

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

function clearOnlineResourceList() {
    onlineResourceFileList.replaceChildren();
}

export function setupOnlineResourceFilesListToggle() {
    toggleOnlineResourceListVisibility(onlineResourceFileInputSwitch.checked);
}

function toggleSimilarSourceNamesError(isErrorVisible) {
    const errorElement = document.querySelector(".online-resource-similar-names-error");
    if (isErrorVisible) {
        return errorElement.classList.remove("d-none");
    }
    return errorElement.classList.add("d-none")

}

export function resetOnlineResourceList() {
    toggleSimilarSourceNamesError(false);
    clearOnlineResourceList();
}

function disableOnlineResourceListFileInputs() {
    const fileInputs = onlineResourceFileList.querySelectorAll("input[type='file']");
    for (const fileInput of fileInputs) {
        fileInput.disabled = true;
    }
}

function checkSourceNamesAreUnique(sourceNames) {
    const sourceNamesGroupedByNormalised = checkForSimilarSourceNames(sourceNames);
    let similarSourceNamesFound = false;
    for (const sourceName in sourceNamesGroupedByNormalised) {
        if (!sourceName) {
            continue;
        }
        const unnormalisedVersionsOfSourceNames = sourceNamesGroupedByNormalised[sourceName];
        if (unnormalisedVersionsOfSourceNames.length <= 1) {
            continue;
        }
        similarSourceNamesFound = true;
        const sourceFileListItems = Array.from(document.querySelectorAll(".online-resource-files-list li")).filter(listItem => {
            const sourceNameInListItem = listItem.querySelector(".source-name").textContent;
            return unnormalisedVersionsOfSourceNames.includes(sourceNameInListItem);
        });
        sourceFileListItems.forEach(listItem => {
            const otherListItems = sourceFileListItems.filter(sourceFileListItem => sourceFileListItem !== listItem);
            listItem.querySelector(".error-similar-source-name .error-text").textContent = `This online resource's name is too similar to the name${otherListItems.length === 1 ? '' : 's'} of ${otherListItems.length} other online resource${otherListItems.length === 1 ? '' : 's'}.`;
            listItem.classList.add("source-name-is-invalid");
        });
    }
    if (similarSourceNamesFound) {
        toggleSimilarSourceNamesError(true);
        disableOnlineResourceListFileInputs(true);
    }
}

export function loadOnlineResourceFiles(metadataFileXmlString) {
    // Reset any errors before proceeding
    // with rest of setup
    toggleSimilarSourceNamesError(false);

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
    
    // Check each online resource name is
    // unique.
    checkSourceNamesAreUnique(Array.from(onlineResources).map(onlineResource => onlineResource.querySelector("name").textContent));

    const onlineResourceFilesInputs = Array.from(document.querySelectorAll("input[name='additional_online_resource_file']"));
    const onlineResourceFiles = onlineResourceFilesInputs.map(input => input.value);
}

onlineResourceFileInputSwitch.addEventListener("change", () => {
    toggleOnlineResourceListVisibility(onlineResourceFileInputSwitch.checked);
});