window.onload = function() {
  //<editor-fold desc="Changeable Configuration Block">

  // the following lines will be replaced by docker/configurator, when it runs in a docker-container
  window.ui = SwaggerUIBundle({
    url: JSON.parse(document.getElementById("api-specification-url").textContent),
    dom_id: '#swagger-ui',
    deepLinking: true,
    filter: true,
    layout: "StandaloneLayout",
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    tryItOutEnabled: true,
  });

  //</editor-fold>
};
