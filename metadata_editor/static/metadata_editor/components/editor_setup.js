export async function setupEditor(editorClass) {
    const editor = new editorClass();
    await editor.runPostSetupActions();
    return editor;
}