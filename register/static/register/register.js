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
                        <div class="d-flex align-items-center">
                            <img src="/static/register/file.svg" alt="file" class="me-3">
                            <input type="hidden" name="file${i}-name" value="${file.name}">
                            <span>${file.name}</span>
                        </div>
                    </div>
                    <div class="col-lg-5">
                        <div class="d-flex flex-wrap">
                            <div class="d-flex align-items-center me-3">
                                <input type="radio" class="me-1" id="radio-is-file${i}-model" name="file${i}-metadata-type" value="model" required>
                                <label for="radio-is-file${i}-model" class="mb-0">Model</label>
                            </div>
                            <div class="d-flex align-items-center">
                                <input type="radio" class="me-1" id="radio-is-file${i}-dataset" name="file${i}-metadata-type" value="dataset" required>
                                <label for="radio-is-file${i}-dataset" class="mb-0">Data Collection</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-2">
                        <div class="d-flex align-items-center">
                            <input type="checkbox" class="me-1" id="checkbox-is-file${i}-executable" name="is-file${i}-executable">
                            <label for="checkbox-is-file${i}-executable" class="mb-0">Executable</label>
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