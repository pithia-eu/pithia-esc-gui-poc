function isTimePeriodBeginBeforeOrEqualToTimePeriodEnd(timePeriodBeginValue, timePeriodEndValue) {
    const beginDateTime = new Date(timePeriodBeginValue).getTime();
    const endDateTime = new Date(timePeriodEndValue).getTime();

    return beginDateTime <= endDateTime;
}

export function alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput) {
    if ((!timePeriodBeginInput.value && !timePeriodBeginInput.required)
        && (!timePeriodEndInput.value && !timePeriodEndInput.required)) {
            timePeriodBeginInput.classList.remove("is-invalid");
            return timePeriodEndInput.classList.remove("is-invalid");
    }
    if (!timePeriodBeginInput.value && !timePeriodBeginInput.required) {
        return timePeriodBeginInput.classList.remove("is-invalid");
    }
    if (!timePeriodEndInput.value && !timePeriodEndInput.required) {
        return timePeriodEndInput.classList.remove("is-invalid");
    }
    if (isTimePeriodBeginBeforeOrEqualToTimePeriodEnd(timePeriodBeginInput.value, timePeriodEndInput.value)) {
        timePeriodBeginInput.classList.remove("is-invalid");
        return timePeriodEndInput.classList.remove("is-invalid");
    }
    timePeriodBeginInput.classList.add("is-invalid");
}

function updateTimePeriodEndMinValue(timePeriodBeginValue, timePeriodEndInput) {
    timePeriodEndInput.min = timePeriodBeginValue;
}

function updateTimePeriodBeginMaxValue(timePeriodEndValue, timePeriodBeginInput) {
    timePeriodBeginInput.max = timePeriodEndValue;
}

export function setupTimePeriodElements(timePeriodBeginInputSelector, timePeriodEndInputSelector) {
    const timePeriodBeginInput = document.querySelector(timePeriodBeginInputSelector);
    const timePeriodEndInput = document.querySelector(timePeriodEndInputSelector);

    if (timePeriodBeginInput.value) {
        updateTimePeriodEndMinValue(timePeriodBeginInput.value, timePeriodEndInput);
    }

    if (timePeriodEndInput.value) {
        updateTimePeriodBeginMaxValue(timePeriodEndInput.value, timePeriodBeginInput);
    }

    timePeriodBeginInput.addEventListener("input", () => {
        updateTimePeriodEndMinValue(timePeriodBeginInput.value, timePeriodEndInput);
    });

    timePeriodEndInput.addEventListener("input", () => {
        updateTimePeriodBeginMaxValue(timePeriodEndInput.value, timePeriodBeginInput);
    });
}