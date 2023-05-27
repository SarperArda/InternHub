const contactDiv = document.getElementById("contact-div");
const contactButton = document.getElementById("contact-button");
const notificationDiv = document.getElementById("notification-div");
const announcementDiv = document.getElementById("announcement-div");
const announcementButton = document.getElementById("announcement-button");
const notificationButton = document.getElementById("notification-button");
const internshipButton = document.getElementById("internship-button");
const internshipDiv = document.getElementById("internship-div");

announcementDiv.hidden = false;
notificationDiv.hidden = true;
contactDiv.hidden = true;
internshipDiv.hidden = true;

contactButton.addEventListener("click", function () {
    announcementDiv.hidden = true;
    notificationDiv.hidden = true;
    contactDiv.hidden = false;
    internshipDiv.hidden = true;
});

announcementButton.addEventListener("click", function () {
    announcementDiv.hidden = false;
    notificationDiv.hidden = true;
    contactDiv.hidden = true;
    internshipDiv.hidden = true;
});

notificationButton.addEventListener("click", function () {
    announcementDiv.hidden = true;
    notificationDiv.hidden = false;
    contactDiv.hidden = true;
    internshipDiv.hidden = true;
});

internshipButton.addEventListener("click", function () {
    announcementDiv.hidden = true;
    notificationDiv.hidden = true;
    contactDiv.hidden = true;
    internshipDiv.hidden = false;
});

function navigateToAnotherPage(page) {
    window.location.href = page;
}