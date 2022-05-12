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
                <div class="row g-lg-4 g-sm-2 py-2">
                    <div class="col-lg-8">
                        <div class="d-flex align-items-center">
                            <img src="/static/register/file.svg" alt="file" class="me-3">
                            <input type="hidden" name="file${i}-name" value="${file.name}">
                            <span class="file-name" title=${file.name}>${file.name}</span>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        Validation progress indicator will appear here
                    </div>
                </div>
            </li>`
        ));
    });
}

const collapseGuidance = document.getElementById('collapse-guidance')
const bsCollapseGuidance = new bootstrap.Collapse(collapseGuidance, {
    toggle: false
});
filesInput.addEventListener("change", event => {
    loadUploadedFilesList();
    bsCollapseGuidance.show();
});

document.getElementById("register-script").addEventListener("load", event => {
    if (filesInput.value !== "") {
        loadUploadedFilesList();
    }
});