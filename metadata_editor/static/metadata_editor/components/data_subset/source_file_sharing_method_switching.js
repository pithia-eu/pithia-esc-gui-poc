import {
    editorForm,
} from "/static/metadata_editor/components/base_editor.js";

const sourceFileSharingMethodCheckbox = editorForm.querySelector("input[name='is_file_uploaded_for_each_online_resource']");


function switchSourceFileSharingMethod(sourcesTab) {
    if (sourceFileSharingMethodCheckbox.checked) {
        sourcesTab.setSourceFileSharingMethodToFileUpload();
    } else {
        sourcesTab.setSourceFileSharingMethodToLinkage();
    }
    return sourcesTab.updateAllTabPaneConditionalRequiredFieldStates();
}

export function setupSourceFileSharingMethodSwitching(sourcesTab) {
    switchSourceFileSharingMethod(sourcesTab);
    sourceFileSharingMethodCheckbox.addEventListener("change", () => {
        switchSourceFileSharingMethod(sourcesTab);
    });
}