import {
    ProjectEditor,
} from "/static/metadata_editor/project_editor.js";
import {
    setupEditor,
} from "/static/metadata_editor/components/editor_setup.js";


window.addEventListener("load", async () => {
    const editor = await setupEditor(ProjectEditor);
});