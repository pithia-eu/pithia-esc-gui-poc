import {
    DynamicEditorTab,
} from "/static/metadata_editor/components/tab_utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/metadata_editor/components/conditional_required_fields.js";


class CapabilitiesTab extends DynamicEditorTab {
    constructor() {
        super(
            "#capabilities-tab",
            "#capabilities-tab-content",
            "#capabilities-tab-content-template",
            ".remove-capability-button",
            "input[name='capabilities_json']",
            "input[name='capabilities_extra_json']",
            "Capability"
        );
    }

    updateTabPaneConditionalRequiredFieldStates(tabPane) {
        const requiredFields = tabPane.querySelectorAll("input[name='capability_name'], select[name='capability_observed_property']");
        const optionalFields = tabPane.querySelectorAll(`
            select[name='capability_dimensionality_instance'],
            select[name='capability_dimensionality_timeline'],
            input[name='capability_cadence'],
            select[name='capability_cadence_units'],
            select[name='capability_vector_representation'],
            select[name='capability_coordinate_system'],
            select[name='capability_units'],
            select[name='capability_qualifier']
        `);
        checkAndSetRequiredAttributesForFields(
            requiredFields,
            optionalFields
        );
    }

    updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane) {
        const requiredFields = tabPane.querySelectorAll("input[name='capability_cadence'], select[name='capability_cadence_units']");
        checkAndSetRequiredAttributesForFields(
            requiredFields
        );
    }

    setup() {
        super.setup();
        const firstTabPane = this.tabContent.querySelector(".tab-pane");
        this.updateTabPaneConditionalRequiredFieldStates(firstTabPane);
        this.updateTabPaneConditionalRequiredCadenceRelatedFieldStates(firstTabPane);        
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        const inputs = tabPane.querySelectorAll("input");
        const selects = tabPane.querySelectorAll("select");
    
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                this.exportTabData();
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
                if (input.name === 'capability_cadence') {
                    this.updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane);
                }
            });
        });
    
        selects.forEach(select => {
            select.addEventListener("change", () => {
                this.exportTabData();
                this.updateTabPaneConditionalRequiredFieldStates(tabPane);
                if (select.name === 'capability_cadence_units') {
                    this.updateTabPaneConditionalRequiredCadenceRelatedFieldStates(tabPane);
                }
            });
        });
    }

    getTabDataAsJson() {
        const capabilities = [];
        const capabilityTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        capabilityTabPanes.forEach(tabPane => {
            const vectorRepresentationSelect = tabPane.querySelector("select[name='capability_vector_representation']");
            const vectorRepresentationSelectedOptions = Array.from(vectorRepresentationSelect.selectedOptions);
            const qualifierSelect = tabPane.querySelector("select[name='capability_qualifier']");
            const qualifierSelectedOptions = Array.from(qualifierSelect.selectedOptions);
            capabilities.push({
                name: tabPane.querySelector("input[name='capability_name']").value,
                observedProperty: tabPane.querySelector("select[name='capability_observed_property']").value,
                dimensionalityInstance: tabPane.querySelector("select[name='capability_dimensionality_instance']").value,
                dimensionalityTimeline: tabPane.querySelector("select[name='capability_dimensionality_timeline']").value,
                cadence: tabPane.querySelector("input[name='capability_cadence']").value,
                cadenceUnits: tabPane.querySelector("select[name='capability_cadence_units']").value,
                vectorRepresentation: vectorRepresentationSelectedOptions.map(option => option.value),
                coordinateSystem: tabPane.querySelector("select[name='capability_coordinate_system']").value,
                units: tabPane.querySelector("select[name='capability_units']").value,
                qualifier: qualifierSelectedOptions.map(option => option.value),
            });
        });
        return capabilities;
    }

    loadPreviousTabData() {
        const previousCapabilities = JSON.parse(this.jsonExportElement.value);
        if (!previousCapabilities) {
            return;
        }
        previousCapabilities.forEach((capability, i) => {
            if (i !== 0) {
                this.createTabAndTabPane();
            }
            const correspondingTabPane = this.tabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
            const selects = correspondingTabPane.querySelectorAll("select");
            correspondingTabPane.querySelector("input[name='capability_name']").value = capability.name;
            correspondingTabPane.querySelector("select[name='capability_observed_property']").value = capability.observedProperty;
            correspondingTabPane.querySelector("select[name='capability_dimensionality_instance']").value = capability.dimensionalityInstance;
            correspondingTabPane.querySelector("select[name='capability_dimensionality_timeline']").value = capability.dimensionalityTimeline;
            correspondingTabPane.querySelector("input[name='capability_cadence']").value = capability.cadence;
            correspondingTabPane.querySelector("select[name='capability_cadence_units']").value = capability.cadenceUnits;
            correspondingTabPane.querySelector("select[name='capability_coordinate_system']").value = capability.coordinateSystem;
            correspondingTabPane.querySelector("select[name='capability_units']").value = capability.units;
            const vectorRepresentationSelect = correspondingTabPane.querySelector("select[name='capability_vector_representation']");
            vectorRepresentationSelect.value = "";
            capability.vectorRepresentation.forEach(component => {
                vectorRepresentationSelect.querySelector(`option[value="${component}"]`).selected = true;
            });
            const qualifierSelect = correspondingTabPane.querySelector("select[name='capability_qualifier']");
            qualifierSelect.value = "";
            capability.qualifier.forEach(qualifier => {
                qualifierSelect.querySelector(`option[value="${qualifier}"]`).selected = true;
            });
    
            selects.forEach(select => {
                window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                    detail: select.id,
                }));
            });
            this.updateTabPaneConditionalRequiredFieldStates(correspondingTabPane);
            this.updateTabPaneConditionalRequiredCadenceRelatedFieldStates(correspondingTabPane); 
        });
        this.disableFirstRemoveTabAndTabPaneButtonIfOnlyOneTab();
    }
}

export function setupCapabilitiesTab() {
    const capabilitiesTab = new CapabilitiesTab();
    capabilitiesTab.setup();
    return capabilitiesTab;
}