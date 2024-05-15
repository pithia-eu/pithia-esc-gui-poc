import {
    DynamicEditorTable,
} from "/static/register_with_support/components/table_utils.js";
import {
    checkAndSetRequiredAttributesForFields,
} from "/static/register_with_support/components/conditional_required_fields.js";

export class CapabilityLinkTimeSpansTable extends DynamicEditorTable {
    constructor(tabId) {
        super(
            `#${tabId} .table-cl-time-spans`,
            `#${tabId} .table-cl-time-spans tbody`,
            `#${tabId} .add-cltsrow-button`,
            `.remove-cltsrow-button`,
            `#capability-link-time-span-row-content-template`,
            `#${tabId} input[name='capability_link_time_spans_json']`
        );
        this.timeSpanBeginPositionInputSelector = "input[name='capability_link_time_span_begin_position']";
        this.timeSpanEndPositionSelectSelector = "select[name='capability_link_time_span_end_position']";
    }

    setupNewRowEventListeners(newRow) {
        super.setupNewRowEventListeners(newRow);

        const fields = Array.from(
            newRow.querySelectorAll(`${this.timeSpanBeginPositionInputSelector}, ${this.timeSpanEndPositionSelectSelector}`)
        );

        const timeSpanBeginPositionInput = newRow.querySelector(this.timeSpanBeginPositionInputSelector);
        timeSpanBeginPositionInput.addEventListener("input", () => {
            checkAndSetRequiredAttributesForFields(fields, fields);
            this.exportTableDataToJsonAndStoreInOutputElement();
        });

        const timeSpanEndPositionSelect = newRow.querySelector(this.timeSpanEndPositionSelectSelector);
        timeSpanEndPositionSelect.addEventListener("change", () => {
            checkAndSetRequiredAttributesForFields(fields, fields);
            this.exportTableDataToJsonAndStoreInOutputElement();
        });
    }

    addRow() {
        const newRow = super.addRow();

        window.dispatchEvent(new CustomEvent("newSelectsAdded", {
            detail: Array.from(newRow.querySelectorAll("select:not([multiple])")).map(select => select.id),
        }));
        this.table.dispatchEvent(new CustomEvent("newTableRowInputsAdded", {
            detail: {
                inputIds: Array.from(newRow.querySelectorAll("input")).map(el => el.id),
                selectIds: Array.from(newRow.querySelectorAll("select")).map(el => el.id),
            },
        }));
    }

    exportTableData() {
        const timeSpanObjects = [];
        this.rows.forEach(row => {
            const timeSpanBeginPositionInput = row.querySelector(this.timeSpanBeginPositionInputSelector);
            const timeSpanEndPositionSelect = row.querySelector(this.timeSpanEndPositionSelectSelector);
            timeSpanObjects.push({
                beginPosition: timeSpanBeginPositionInput.value,
                endPosition: timeSpanEndPositionSelect.value,
            });
        });
        return timeSpanObjects;
    }

    exportTableDataToJsonAndStoreInOutputElement() {
        super.exportTableDataToJsonAndStoreInOutputElement();
        const inputEvent = new Event("input", {
            bubbles: true,
        });
        this.jsonOutputElement.dispatchEvent(inputEvent);
    }

    loadPreviousData() {
        const previousData = JSON.parse(this.jsonOutputElement.value);
        if (!previousData) {
            return;
        }
        previousData.forEach((timeSpan, i) => {
            if (i !== 0) {
                this.addRow();
            }
            const timeSpanBeginPosition = timeSpan.beginPosition;
            const timeSpanEndPosition = timeSpan.endPosition;
            const correspondingRow = this.tableBody.querySelector(`tr:nth-of-type(${i + 1})`);

            // Time span begin position
            const timeSpanBeginPositionInput = correspondingRow.querySelector(this.timeSpanBeginPositionInputSelector);
            timeSpanBeginPositionInput.value = timeSpanBeginPosition;

            // Time span end position (indeterminate)
            const timeSpanEndPositionSelect = correspondingRow.querySelector(this.timeSpanEndPositionSelectSelector);
            timeSpanEndPositionSelect.value = timeSpanEndPosition;
            window.dispatchEvent(new CustomEvent("selectOptionsSetProgrammatically", {
                detail: timeSpanEndPositionSelect.id,
            }));

            const conditionalRequiredFields = Array.from(correspondingRow.querySelectorAll(`${this.timeSpanBeginPositionInputSelector}, ${this.timeSpanEndPositionSelectSelector}`));
            checkAndSetRequiredAttributesForFields(
                conditionalRequiredFields,
                conditionalRequiredFields
            );
        });
    }
}