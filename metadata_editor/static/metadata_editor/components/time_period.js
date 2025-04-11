function isTimePeriodBeginBeforeOrEqualToTimePeriodEnd(timePeriodBeginValue, timePeriodEndValue) {
    const beginDateTime = new Date(timePeriodBeginValue).getTime();
    const endDateTime = new Date(timePeriodEndValue).getTime();

    return beginDateTime <= endDateTime;
}

export function alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput) {
    if (!timePeriodBeginInput.value) {
        timePeriodBeginInput.classList.remove("is-invalid");
        return;
    }
    if (!timePeriodEndInput.value) {
        timePeriodBeginInput.classList.remove("is-invalid");
        return;
    }
    if (isTimePeriodBeginBeforeOrEqualToTimePeriodEnd(timePeriodBeginInput.value, timePeriodEndInput.value)) {
        timePeriodBeginInput.classList.remove("is-invalid");
        return;
    }
    document.querySelector(`#invalid-feedback-${timePeriodBeginInput.id}`).textContent = "The begin time cannot be later than the end time.";
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
        alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput);
    }

    if (timePeriodEndInput.value) {
        updateTimePeriodBeginMaxValue(timePeriodEndInput.value, timePeriodBeginInput);
        alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput);
    }

    timePeriodBeginInput.addEventListener("input", () => {
        updateTimePeriodEndMinValue(timePeriodBeginInput.value, timePeriodEndInput);
        alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput);
    });

    timePeriodEndInput.addEventListener("input", () => {
        updateTimePeriodBeginMaxValue(timePeriodEndInput.value, timePeriodBeginInput);
        alertIfTimePeriodIsInvalid(timePeriodBeginInput, timePeriodEndInput);
    });
}