// static/js/navbar.js
function loadNavbar() {
    const navbarHTML = `
        <nav class="navbar navbar-expand-lg navbar-red">
            <div class="container">
                <a class="navbar-brand" href="/">Blood Donation System</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/donor-registration">Donor Registration/Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/admin-login">Admin Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/blood-request">Blood Request</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    `;
    document.getElementById('navbar').innerHTML = navbarHTML;
}

// Call the function to load the navbar
window.onload = loadNavbar;
