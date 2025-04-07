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

    tabPaneControlEventHandlerActions(tabPane) {
        this.exportTabData();
    }

    setupTabPaneEventListeners(tabPane) {
        super.setupTabPaneEventListeners(tabPane);
        setupTimePeriodElements(`#${tabPane.id} ${this.timeInstantBeginPositionInputSelector}`, `#${tabPane.id} ${this.timeInstantEndPositionInputSelector}`);

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