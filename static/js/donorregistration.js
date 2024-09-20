document.addEventListener('DOMContentLoaded', function () {
    // Auto-detect location and populate latitude and longitude separately
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            document.getElementById('latitude').value = position.coords.latitude;
            document.getElementById('longitude').value = position.coords.longitude;
        }, function (error) {
            alert('Error detecting location. Please allow location access.');
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }

    // Handle form submission
    document.getElementById('donorForm').addEventListener('submit', function (event) {
        const weight = document.getElementById('weight').value;
        const age = document.getElementById('age').value;

        // Custom validation for weight and age
        if (weight < 50 || age < 18) {
            alert('Minimum weight is 50 kg and minimum age is 18 years for blood donation.');
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});
