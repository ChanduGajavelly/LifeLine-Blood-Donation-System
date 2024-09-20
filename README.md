
# Blood Donation System

This is a web-based application designed to facilitate blood donor registrations, manage donor data, and allow administrators to filter and search donors. The application is built using Flask for the backend, MySQL for the database, and HTML/CSS for the frontend with JavaScript for interactive features.

## Features
- Blood donor registration with personal and medical details
- Donor login and search capabilities
- Admin login to manage donors and handle blood requests
- Geolocation auto-detection for donors to record latitude and longitude
- User-friendly form validation with JavaScript
- Responsive design with Bootstrap and TailwindCSS

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap, Tailwind), JavaScript
- **Database**: MySQL
- **Other**: Geolocation API, AJAX, Flask-Session

## Installation and Setup Instructions

### Prerequisites
Make sure you have the following installed on your system:
- Python 3.x
- MySQL server
- pip (Python package installer)

### Setup Instructions
1. Clone this repository to your local machine:
   ```bash
   git clone <your-repository-url>
   cd <your-repository-folder>
   ```
2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the MySQL database:
   - Create a new MySQL database called `blood_donor_db`.
   - Run the following SQL commands to create the `donors` and `admins` tables:

   ```sql
   CREATE TABLE donors (
       id INT NOT NULL AUTO_INCREMENT,
       name VARCHAR(100),
       weight FLOAT,
       age INT,
       gender VARCHAR(20),
       blood_group VARCHAR(10),
       phone VARCHAR(10),
       pincode VARCHAR(6),
       chronic_disease VARCHAR(5),
       latitude VARCHAR(50),
       longitude VARCHAR(50),
       PRIMARY KEY (id)
   );

   CREATE TABLE admins (
       admin_id INT NOT NULL AUTO_INCREMENT,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       phone_number VARCHAR(15),
       avatar MEDIUMBLOB,
       PRIMARY KEY (admin_id)
   );
   ```

5. Update environment variables:
   - You can create a `.env` file to store your environment variables (e.g., database credentials):
   ```bash
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=<your-password>
   DB_NAME=blood_donor_db
   SECRET_KEY=<your-secret-key>
   ```

6. Run the Flask application:
   ```bash
   flask run
   ```
   The application should now be running at `http://localhost:5000`.

## Usage
- Navigate to the home page to register as a donor or log in as an admin.
- Admins can filter donors by blood group, gender, age, and location.
- Donors can view their registration details after signing up.

## Contributing
If you'd like to contribute to this project, feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.
