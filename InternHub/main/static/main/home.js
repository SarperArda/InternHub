const contactDiv = document.getElementById("contact-div");
const contactButton = document.getElementById("contact-button");
const notificationDiv = document.getElementById("notification-div");
const announcementDiv = document.getElementById("announcement-div");
const announcementButton = document.getElementById("announcement-button");
const notificationButton = document.getElementById("notification-button");

announcementDiv.hidden = false;
notificationDiv.hidden = true;
contactDiv.hidden = true;

contactButton.addEventListener("click", function () {
    announcementDiv.hidden = true;
    notificationDiv.hidden = true;
    contactDiv.hidden = false;
});

announcementButton.addEventListener("click", function () {
    announcementDiv.hidden = false;
    notificationDiv.hidden = true;
    contactDiv.hidden = true;
});

notificationButton.addEventListener("click", function () {
    announcementDiv.hidden = true;
    notificationDiv.hidden = false;
    contactDiv.hidden = true;
});
