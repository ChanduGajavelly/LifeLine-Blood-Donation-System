document.addEventListener('DOMContentLoaded', function () {
    // Form validation and showing loading spinner
    var forms = document.getElementsByClassName('needs-validation');
    Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');

            // Show loading spinner
            if (form.checkValidity() === true) {
                document.getElementById('loading').style.display = 'block';
            }
        }, false);
    });

    // Sign up form validation
    var signUpForm = document.getElementById('signUpForm');
    if (signUpForm) {
        signUpForm.addEventListener('submit', function (event) {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;

            if (username === '' || password === '') {
                alert('Please fill in all fields.');
                event.preventDefault();
            }
        });
    }
});
