// Example of JavaScript functionality (could be for form validation or other interactive features)
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded!');
});

 // Initialize EmailJS with your user ID
     emailjs.init("YOUR_USER_ID");

       // Handle form submission
    document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Gather form data
    const formData = new FormData(this);

 // Send the email using EmailJS
      emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', formData)
         .then(function(response) {
             // On success, show success message
            document.getElementById('response-message').style.display = 'block';
            document.getElementById('contact-form').reset();
            document.getElementById('error-message').style.display = 'none';
        }, function(error) {
            // On error, show error message
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('response-message').style.display = 'none';
        });
   });

