import {
    setupLocalIdAndNamespaceRelatedEventListeners,
} from "/static/metadata_editor/components/localid_validation.js";


export const NewRegistrationEditorMixin = (Base) => class extends Base {
    async setupNewRegistrationEditingFunctionalities() {
        await setupLocalIdAndNamespaceRelatedEventListeners();
    }
}