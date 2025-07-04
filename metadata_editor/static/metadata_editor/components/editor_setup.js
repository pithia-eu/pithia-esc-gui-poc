export async function setupEditor(editorClass) {
    const editor = new editorClass();
    await editor.runAfterInitialEditorSetup();
    return editor;
}