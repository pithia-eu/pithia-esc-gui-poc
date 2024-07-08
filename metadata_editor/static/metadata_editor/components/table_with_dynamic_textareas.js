import {
    DynamicEditorTable,
} from "/static/metadata_editor/components/table_utils.js";


export class DynamicEditorTableWithTextArea extends DynamicEditorTable {
    setupDynamicTextAreaForNewRow(newRow, textareaSelector) {
        const dynamicTextarea = newRow.querySelector(textareaSelector);
        const dynamicTextareaFacade = newRow.querySelector(`${textareaSelector} ~ div`);
    
        dynamicTextarea.addEventListener("focus", () => {
            dynamicTextarea.style.height = dynamicTextarea.scrollHeight + "px";
        });
        
        dynamicTextarea.addEventListener("input", () => {
            dynamicTextarea.style.height = dynamicTextarea.scrollHeight + "px";
            dynamicTextareaFacade.innerHTML = dynamicTextarea.value;
            this.exportTableDataToJsonAndStoreInOutputElement();
        });
        
        dynamicTextarea.addEventListener("blur", () => {
            dynamicTextarea.removeAttribute("style");
        });
    }
}