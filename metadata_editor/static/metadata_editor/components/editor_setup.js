export async function setupEditor(editorClass) {
    const editor = new editorClass();
    editor.setup();
    await editor.runAfterInitialEditorSetup();
    return editor;
}