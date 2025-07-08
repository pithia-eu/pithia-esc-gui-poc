import {
    PlatformEditor,
} from "/static/metadata_editor/platform_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


window.addEventListener("load", async () => {
    const editor = await setupEditor(PlatformEditor);
});