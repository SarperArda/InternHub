const submitButton = document.getElementById("submit-button");
const feedbacksButton = document.getElementById("feedbacks-button");
const contactButton = document.getElementById("contact-button");

const announcementDiv = document.getElementById("announcement-div");
const submitDiv = document.getElementById("submit-div");
const feedbackDiv = document.getElementById("feedback-div");
const contactDiv = document.getElementById("contact-div");

announcementDiv.hidden = false;
submitDiv.hidden = true;
feedbackDiv.hidden = true;
contactDiv.hidden = true;

submitButton.addEventListener("click", function() {
    announcementDiv.hidden = true;
    submitDiv.hidden = false;
    feedbackDiv.hidden = true;
    contactDiv.hidden = true;
});

feedbacksButton.addEventListener("click", function() {
    announcementDiv.hidden = true;
    submitDiv.hidden = true;
    feedbackDiv.hidden = false;
    contactDiv.hidden = true;
});

contactButton.addEventListener("click", function() {
    announcementDiv.hidden = true;
    submitDiv.hidden = true;
    feedbackDiv.hidden = true;
    contactDiv.hidden = false;
});
