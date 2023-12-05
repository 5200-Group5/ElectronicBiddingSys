document.addEventListener('DOMContentLoaded', function () {
  const saveButton = document.getElementById('save-button');
  const reportButton = document.getElementById("report-button");
  const reportModal = document.getElementById("report-modal");
  const closeModalButton = document.getElementById('close-modal');
  const reportForm = document.getElementById('report-form');

  saveButton.addEventListener('click', function () {
      saveChanges();
  });

  reportButton.addEventListener('click', function () {
    reportButton.style.display='none';
      openReportModal();
  });

  closeModalButton.addEventListener('click', function () {
      closeReportModal();
  });

  reportForm.addEventListener('submit', function (event) {
      event.preventDefault();
      submitReport();
  });

  function saveChanges() {
      // Existing saveChanges logic...
  }

  function openReportModal() {
      reportModal.style.display = 'block';
  }

  function closeReportModal() {
      reportModal.style.display = 'none';
  }

    // Existing code...

    function submitReport() {
        const reportMessage = document.getElementById('report-message').value;

        const apiUrl = '/account/report-issue/';
        const formData = new FormData();
        formData.append('message', reportMessage);

        // Make an AJAX request to the Django backend
        fetch(apiUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        })
        .then(data => {
            console.log(data);
            closeReportModal();
            // You can add additional logic here, such as showing a success message
        })
        .catch(error => {
            console.error('Error submitting report:', error);
            // You can add error handling logic here, such as showing an error message to the user
        });
    }
});
