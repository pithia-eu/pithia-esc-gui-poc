import {
    DynamicEditorTab,
} from "/static/metadata_editor/components/tab_utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";


class CitationsTab extends DynamicEditorTab {
    constructor() {
        super(
            "#citations-tab",
            "#citations-tab-content",
            "#citations-tab-content-template",
            ".remove-citation-button",
            "input[name='citations_json']",
            "input[name='citations_extra_json']",
            "Documentation"
        );
        this.requiredFieldsSelector = "input[name='citation_title'], input[name='citation_publication_date']";
        this.optionalFieldsSelector = `
            textarea[name='other_citation_details'],
            input[name='citation_doi'],
            input[name='citation_linkage_url']
        `;
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        const requiredFields = tabPane.querySelectorAll(this.requiredFieldsSelector);
        const optionalFields = tabPane.querySelectorAll(this.optionalFieldsSelector);
        checkAndSetRequiredAttributesForFields(
            requiredFields,
            optionalFields
        );
    }

    setup() {
        super.setup();
        const firstTabPane = this.tabContent.querySelector(".tab-pane");
        this.updateTabPaneConditionalRequiredFieldStates(firstTabPane);
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        const inputsAndTextareas = tabPane.querySelectorAll("input, textarea");
    
        inputsAndTextareas.forEach(inputOrTextarea => {
            inputOrTextarea.addEventListener("input", () => {
                this.exportTabData();
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
            });
        });
    }

    getTabDataAsJson() {
        const citations = [];
        const citationTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        citationTabPanes.forEach(tabPane => {
            citations.push({
                title: tabPane.querySelector("input[name='citation_title']").value,
                publicationDate: tabPane.querySelector("input[name='citation_publication_date']").value,
                doi: tabPane.querySelector("input[name='citation_doi']").value,
                otherCitationDetails: tabPane.querySelector("textarea[name='other_citation_details']").value,
                linkageUrl: tabPane.querySelector("input[name='citation_linkage_url']").value,
            });
            console.log('citations', citations);
        });
        return citations;
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
        const previousCitations = JSON.parse(this.jsonExportElement.value);
        if (!previousCitations) {
            return;
        }
        previousCitations.forEach((citation, i) => {
            if (i !== 0) {
                this.createTabAndTabPane();
            }
            const correspondingTabPane = this.tabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
            correspondingTabPane.querySelector("input[name='citation_title']").value = citation.title;
            correspondingTabPane.querySelector("input[name='citation_publication_date']").value = citation.publicationDate;
            correspondingTabPane.querySelector("input[name='citation_doi']").value = citation.doi;
            correspondingTabPane.querySelector("input[name='citation_linkage_url']").value = citation.linkageUrl;
            correspondingTabPane.querySelector("textarea[name='other_citation_details']").value = citation.otherCitationDetails;
            this.updateTabPaneConditionalRequiredFieldStates(correspondingTabPane);
        });
        this.disableFirstRemoveTabAndTabPaneButtonIfOnlyOneTab();
    }
}

export function setupCitationsTab() {
    const citationsTab = new CitationsTab();
    citationsTab.setup();
    return citationsTab;
}