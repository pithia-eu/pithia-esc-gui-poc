import {
    DynamicEditorTab,
} from "/static/metadata_editor/components/tab_utils.js";
import {
    setupTimePeriodElements,
} from "/static/metadata_editor/components/time_period.js";


export class TimePeriodsTab extends DynamicEditorTab {
    constructor() {
        super(
            "#time-periods-tab",
            "#time-periods-tab-content",
            "#time-periods-tab-pane-content-template",
            ".remove-time-period-button",
            "input[name='time_periods_json']",
            "input[name='time_periods_extra_json']",
            "Time Period"
        );
        // Time period ID
        this.timePeriodIdInputSelector = "input[name='time_period_id']";
        // Beginning of time period
        this.timeInstantBeginIdInputSelector = "input[name='time_instant_begin_id']";
        this.timeInstantBeginPositionInputSelector = "input[name='time_instant_begin_position']";
        // End of time period
        this.timeInstantEndIdInputSelector = "input[name='time_instant_end_id']";
        this.timeInstantEndPositionInputSelector = "input[name='time_instant_end_position']";
    }

    #updateInvalidFeedbackForInput(input) {
        document.querySelector(`#invalid-feedback-${input.id}`).textContent = "IDs must be unique.";
    }

    #markInputAsInvalid(input) {
        input.classList.add("is-invalid");
    }

    #resetInvalidInput(input) {
        input.classList.remove("is-invalid");
    }

    #alertIfDuplicateIds() {
        const idInputsInTab = Array.from(this.tabContent.querySelectorAll(`${this.timePeriodIdInputSelector}, ${this.timeInstantBeginIdInputSelector}, ${this.timeInstantEndIdInputSelector}`));
        const idInputsInTabMarkedAsInvalid = Array.from(this.tabContent.querySelectorAll(`${this.timePeriodIdInputSelector}.is-invalid, ${this.timeInstantBeginIdInputSelector}.is-invalid, ${this.timeInstantEndIdInputSelector}.is-invalid`));
        // Reset styling of fields that are marked as invalid
        idInputsInTabMarkedAsInvalid.forEach(input => this.#resetInvalidInput(input));
        // Find and mark fields that have duplicate IDs
        for (const input of idInputsInTab) {
            // If fields are empty, continue
            if (!input.value.trim()) {
                continue;
            }
            const otherInputsWithSameId = idInputsInTab.filter(otherInput => input.id !== otherInput.id && input.value.trim() === otherInput.value.trim());
            // If no other duplicate IDs, continue
            if (!otherInputsWithSameId.length) {
                continue;
            }
            // If duplicate IDs, mark fields as invalid
            this.#updateInvalidFeedbackForInput(input);
            this.#markInputAsInvalid(input);
            otherInputsWithSameId.forEach(otherInput => {
                this.#updateInvalidFeedbackForInput(otherInput);
                this.#markInputAsInvalid(otherInput);
            });
        }
    }

    tabPaneControlEventHandlerActions(tabPane) {
        this.exportTabData();
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        setupTimePeriodElements(`#${tabPane.id} ${this.timeInstantBeginPositionInputSelector}`, `#${tabPane.id} ${this.timeInstantEndPositionInputSelector}`);
        this.#alertIfDuplicateIds();

        const idInputsInTab = this.tabContent.querySelectorAll(`${this.timePeriodIdInputSelector}, ${this.timeInstantBeginIdInputSelector}, ${this.timeInstantEndIdInputSelector}`);
        idInputsInTab.forEach(input => {
            input.addEventListener("input", () => {
                this.#alertIfDuplicateIds();
            });
        });

        const inputs = Array.from(tabPane.querySelectorAll("input"));
        inputs.forEach(input => {
            input.addEventListener("input", () => {
                this.tabPaneControlEventHandlerActions(tabPane);
            });
        });
    }

    getTabPaneData(tabPane) {
        const timePeriodIdInput = tabPane.querySelector(this.timePeriodIdInputSelector);
        const timeInstantBeginIdInput = tabPane.querySelector(this.timeInstantBeginIdInputSelector);
        const timeInstantBeginPositionInput = tabPane.querySelector(this.timeInstantBeginPositionInputSelector);
        const timeInstantEndIdInput = tabPane.querySelector(this.timeInstantEndIdInputSelector);
        const timeInstantEndPositionInput = tabPane.querySelector(this.timeInstantEndPositionInputSelector);
        return {
            timePeriodId: timePeriodIdInput.value,
            timeInstantBeginId: timeInstantBeginIdInput.value,
            timeInstantBeginPosition: timeInstantBeginPositionInput.value,
            timeInstantEndId: timeInstantEndIdInput.value,
            timeInstantEndPosition: timeInstantEndPositionInput.value,
        };
    }

    getTabDataAsJson() {
        const timePeriods = [];
        const timePeriodTabPanes = this.tabContent.querySelectorAll(".tab-pane");
        timePeriodTabPanes.forEach(tabPane => {
            const tabPaneData = this.getTabPaneData(tabPane);
            timePeriods.push(tabPaneData);
        });
        return timePeriods;
    }

    loadPreviousTabPaneData(timePeriod, correspondingTabPane) {
        // Time period ID
        const timePeriodIdInput = correspondingTabPane.querySelector(this.timePeriodIdInputSelector);
        timePeriodIdInput.value = timePeriod.timePeriodId;

        // Beginning of time period
        const timeInstantBeginIdInput = correspondingTabPane.querySelector(this.timeInstantBeginIdInputSelector);
        timeInstantBeginIdInput.value = timePeriod.timeInstantBeginId;
        const timeInstantBeginPositionInput = correspondingTabPane.querySelector(this.timeInstantBeginPositionInputSelector);
        timeInstantBeginPositionInput.value = timePeriod.timeInstantBeginPosition;

        // End of time period
        const timeInstantEndIdInput = correspondingTabPane.querySelector(this.timeInstantEndIdInputSelector);
        timeInstantEndIdInput.value = timePeriod.timeInstantEndId;
        const timeInstantEndPositionInput = correspondingTabPane.querySelector(this.timeInstantEndPositionInputSelector);
        timeInstantEndPositionInput.value = timePeriod.timeInstantEndPosition;
    }

    loadPreviousTabData() {
        super.loadPreviousTabData();
        const previousTimePeriods = JSON.parse(this.jsonExportElement.value);
        if (!previousTimePeriods) {
            return;
        }
        previousTimePeriods.forEach((timePeriod, i) => {
            if (i !== 0) {
                this.createTabAndTabPane();
            }
            const correspondingTabPane = this.tabContent.querySelector(`.tab-pane:nth-of-type(${i + 1})`);
            this.loadPreviousTabPaneData(timePeriod, correspondingTabPane);
        });
    }
}

export function setupTimePeriodsTab() {
    const timePeriodsTab = new TimePeriodsTab();
    timePeriodsTab.setup();
    return timePeriodsTab;
}