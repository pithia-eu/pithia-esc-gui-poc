// Source for htmlToElement function: https://stackoverflow.com/a/35385518
function htmlToElement(html) {
    const template = document.createElement("template");
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

const filesInput = document.getElementById("id_files");
function loadUploadedFilesList() {
    const files = Array.from(filesInput.files);
    const uploadedFilesList = document.querySelector(".list-uploaded-files");
    uploadedFilesList.innerHTML = "";
    files.forEach((file, i) => {
        uploadedFilesList.append(htmlToElement(
            `<li class="list-group-item">
                <div class="row g-2 py-2">
                    <div class="col-lg-5">
                        <div class="d-flex align-items-center"><img src="/static/register/file.svg" alt="file" class="me-3"><span>${file.name}</span></div>
                    </div>
                    <div class="col-lg-5">
                        <div class="d-flex flex-wrap">
                            <div class="d-flex align-items-center me-3">
                                <input type="radio" class="me-1" id="radio-model-${file.name}" name="${file.name}-metadata-type" value="model">
                                <label for="radio-model-${file.name}" class="mb-0">Model</label>
                            </div>
                            <div class="d-flex align-items-center">
                                <input type="radio" class="me-1" id="radio-dataset-${file.name}" name="${file.name}-metadata-type" value="dataset">
                                <label for="radio-dataset-${file.name}" class="mb-0">Data Collection</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-2">
                        <div class="d-flex align-items-center">
                            <input type="checkbox" class="me-1" id="checkbox-is-executable-${file.name}" name="checkbox-is-executable-${file.name}">
                            <label for="checkbox-is-executable-${file.name}" class="mb-0">Executable</label>
                        </div>
                    </div>
                </div>
            </li>`
        ));
    });
}

filesInput.addEventListener("change", event => {
    loadUploadedFilesList();
});

document.getElementById("register-script").addEventListener("load", event => {
    if (filesInput.value !== "") {
        loadUploadedFilesList();
    }
});