import {
    MetadataFileValidator
} from "/static/inline_metadata_validation.js";
const existing_metadata_id = JSON.parse(document.getElementById("resource-id").textContent);

class MetadataFileUpdateValidator extends MetadataFileValidator {
    constructor() {
        super()
    }

    async validateWithServer(metadataFile) {
        const validationUrl = JSON.parse(document.getElementById("inline_validation_url").textContent);
        const response = await fetch(`${validationUrl}?` + new URLSearchParams({
            xml_file_string: metadataFile.xmlFileString,
            xml_file_name: metadataFile.name,
            existing_metadata_id: existing_metadata_id,
        }));
        const results = await response.json();
        return results;
    }
}

window.addEventListener("load", async () => {
    const validator = new MetadataFileUpdateValidator();
});