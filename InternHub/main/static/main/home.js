document.getElementById("submit-button").addEventListener("click", function() {
  loadContent("reports.html", "middle-column");
});

document.getElementById("feedbacks-button").addEventListener("click", function() {
  loadContent("feedbacks.html", "middle-column");
});

function loadContent(url, targetId) {
  var targetElement = document.getElementById(targetId);
  fetch(url)
    .then(response => response.text())
    .then(content => {
      targetElement.innerHTML = content;
    })
    .catch(error => {
      console.error("Error loading content:", error);
    });
}