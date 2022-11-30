const xmlDownloadButton = document.querySelector(".xml-file-download-btn");
const xmlFileContent = document.querySelector(".xml-display-area").textContent;
const xmlFileName = `${document.querySelector("#resource-localid").value}.xml`;


function setupXmlFileDownloadLink() {
    const xmlFile = new Blob([xmlFileContent], {
        type: "xml"
    });
    if (window.navigator.msSaveOrOpenBlob) {
        return xmlDownloadButton.addEventListener("click", event => {
            window.navigator.msSaveOrOpenBlob(xmlFile, xmlFileName);
        });
    } else {
        const url = URL.createObjectURL(xmlFile);
        xmlDownloadButton.href = url;
        xmlDownloadButton.download = xmlFileName;
    }
    xmlDownloadButton.classList.remove("disabled");
    xmlDownloadButton.setAttribute("aria-disabled", "false");
}

function pageSetup() {
    setupXmlFileDownloadLink();
}

window.onload = pageSetup;