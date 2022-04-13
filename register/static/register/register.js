// Source for htmlToElement function: https://stackoverflow.com/a/35385518
function htmlToElement(html) {
    const template = document.createElement("template");
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

const filesInput = document.getElementById("id_files");
filesInput.addEventListener("change", event => {
    const files = Array.from(filesInput.files);
    const uploadedFilesList = document.querySelector(".list-uploaded-files");
    uploadedFilesList.innerHTML = "";
    files.forEach(file => {
        uploadedFilesList.append(htmlToElement(
            `<li class="list-group-item">
                <span class="metadata-file-for-reg-name">${file.name}</span>
                <div class="d-flex justify-content-around flex-wrap">
                    <div class="d-flex">
                        <input type="radio" class="me-1" id="radio-model-${file.name}" name="${file.name}-metadata-type" value="model">
                        <label for="radio-model-${file.name}">Model
                    </div>
                    <div class="d-flex">
                        <input type="radio" class="me-1" id="radio-dataset-${file.name}" name="${file.name}-metadata-type" value="dataset">
                        <label for="radio-dataset-${file.name}">Data Collection
                    </div>
                </div>
            </li>`
        ));
    });
});