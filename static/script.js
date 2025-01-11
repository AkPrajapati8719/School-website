
// Function to change the brand name dynamically
function changeBrandName() {
    const brands = ["S.V. Convent School", "Vivekanand Vidhya Vihar School"];
    let currentBrandIndex = 0;
    const brandElement = document.getElementById("brand-name");

    // Change brand name every 3 seconds
    setInterval(function() {
        brandElement.textContent = brands[currentBrandIndex];
        currentBrandIndex = (currentBrandIndex + 1) % brands.length;
    }, 3000); // Change every 3 seconds
}

// Call the function when the page loads
window.onload = changeBrandName;



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

