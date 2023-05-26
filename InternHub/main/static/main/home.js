// Get the button elements
var submitButton = document.getElementById("submit-button");
var feedbacksButton = document.getElementById("feedbacks-button");

// Get the div elements
var announcementDiv = document.getElementById("announcement-div");
var submitDiv = document.getElementById("submit-div");
var feedbackDiv = document.getElementById("feedback-div");

// Set the initial visibility
announcementDiv.hidden = false;
submitDiv.hidden = true;
feedbackDiv.hidden = true;

// Add click event listeners to the buttons
submitButton.addEventListener("click", function() {
    announcementDiv.hidden = true;
    submitDiv.hidden = false;
    feedbackDiv.hidden = true;
});

feedbacksButton.addEventListener("click", function() {
    announcementDiv.hidden = true;
    submitDiv.hidden = true;
    feedbackDiv.hidden = false;
});

