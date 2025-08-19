import {
    ComputationCapabilitiesEditor,
} from "/static/metadata_editor/computation_capabilities_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


window.addEventListener("load", async () => {
    const editor = await setupEditor(ComputationCapabilitiesEditor);
});