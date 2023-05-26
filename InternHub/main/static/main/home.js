function changeContent(buttonId) {
  var middleColumn = document.getElementById('middle-column');
  var middleColumnTitle = document.getElementById('announcements');

  // Replace the content based on the button clicked
  if (buttonId === 1) {
    middleColumnTitle.textContent = 'Submit';
    middleColumn.innerHTML = `
      <p>This is the content for the Submit button.</p>
    `;
  } else if (buttonId === 2) {
    middleColumnTitle.textContent = 'Feedbacks';
    middleColumn.innerHTML = `
      <p>This is the content for the Feedbacks button.</p>
    `;
  }
}
  