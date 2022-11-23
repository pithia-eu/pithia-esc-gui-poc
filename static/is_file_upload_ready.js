import {
    isEachFileValid
} from "/static/file_upload.js";

export function enableSubmitButtonIfReady() {
    let isFileReadyToSubmit = isEachFileValid;
    document.querySelector("button[type='submit']").disabled = !isFileReadyToSubmit;
}