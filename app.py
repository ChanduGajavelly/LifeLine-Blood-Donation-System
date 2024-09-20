from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
import math
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Secure session cookie settings
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
)

# Database connection
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'tiger'),
            database=os.environ.get('DB_NAME', 'blood_donor_db')
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/donor-registration')
def donor_registration():
    return render_template('donorregistration.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Retrieve form data
        name = request.form['name']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['bloodGroup']
        phone = request.form['phone']
        pincode = request.form['pincode']
        chronic_disease = request.form['chronicDisease']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # Validate required fields
        if not all([name, weight, age, gender, blood_group, phone, pincode]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('donor_registration'))

        db = get_db_connection()
        if db is None:
            flash('Database connection failed.', 'danger')
            return redirect(url_for('donor_registration'))

        with db.cursor() as cursor:
            sql = """INSERT INTO donors (name, weight, age, gender, blood_group, phone, pincode, chronic_disease, latitude, longitude)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (name, weight, age, gender, blood_group, phone, pincode, chronic_disease, latitude, longitude)
            cursor.execute(sql, val)
            db.commit()

        flash('Donor registered successfully!', 'success')
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('An error occurred while saving the data.', 'danger')
    except Exception as e:
        print(f"Error: {e}")
        flash('An unexpected error occurred.', 'danger')
    finally:
        if db:
            db.close()

    return redirect(url_for('donor_registration'))

@app.route('/donor-signup')
def donor_signup():
    return render_template('donorsignup.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        db = get_db_connection()
        if db is None:
            flash('Database connection failed.', 'danger')
            return render_template('adminlogin.html')
        try:
            # Retrieve the admin by username
            with db.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
                admin = cursor.fetchone()

            # If admin exists and plain-text password matches
            if admin and admin['password'] == password:
                # Set session variables
                session['admin'] = admin['username']
                flash('Logged in successfully!', 'success')
                return render_template('filterdonors.html')
            else:
                flash('Invalid username or password.', 'danger')
                return render_template('adminlogin.html')
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred while processing your login.', 'danger')
        finally:
            db.close()
            
    return render_template('adminlogin.html')

@app.route('/search', methods=['POST'])
def search_donor():
    name = request.form['name']
    phone = request.form['phone']

    db = get_db_connection()
    if db is None:
        flash('Database connection failed.', 'danger')
        return render_template('donordetails.html')

    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM donors WHERE name = %s AND phone = %s", (name, phone))
        donor = cursor.fetchone()

    db.close()

    if donor:
        return render_template('donordetails.html', donor=donor)
    else:
        flash('No donor found with the provided details.', 'warning')
        return render_template('donordetails.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return "Admin Dashboard"

@app.route('/blood-request')
def blood_request():
    db = get_db_connection()
    if db is None:
        flash('Database connection failed.', 'danger')
        return render_template('bloodrequest.html', admins=[])

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT username, phone_number, avatar FROM admins")
            admins = cursor.fetchall()

        admins_with_images = []
        for admin in admins:
            username, phone_number, avatar_blob = admin
            avatar_data_uri = base64.b64encode(avatar_blob).decode('utf-8') if avatar_blob else "https://via.placeholder.com/100"
            admins_with_images.append({
                'username': username,
                'phone_number': phone_number,
                'avatar': f'data:image/jpeg;base64,{avatar_data_uri}'
            })

        return render_template('bloodrequest.html', admins=admins_with_images)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('An error occurred while fetching data.', 'danger')
        return render_template('bloodrequest.html', admins=[])
    finally:
        db.close()

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371 * c  # Radius of Earth in kilometers

@app.route('/filter-donors', methods=['GET', 'POST'])
def filter_donors():
    if request.method == 'POST':
        blood_group = request.form.get('blood_group')
        gender = request.form.get('gender')
        age = request.form.get('age')
        user_latitude = request.form.get('latitude')
        user_longitude = request.form.get('longitude')

        query = "SELECT * FROM donors WHERE 1=1"
        values = []

        if blood_group:
            query += " AND blood_group = %s"
            values.append(blood_group)
        if gender:
            query += " AND gender = %s"
            values.append(gender)
        if age:
            query += " AND age = %s"
            values.append(age)

        db = get_db_connection()
        if db is None:
            flash('Database connection failed.', 'danger')
            return render_template('filterdonors.html', donors=[])

        try:
            with db.cursor(dictionary=True) as cursor:
                cursor.execute(query, values)
                donors = cursor.fetchall()

            if user_latitude and user_longitude:
                user_latitude = float(user_latitude)
                user_longitude = float(user_longitude)

                for donor in donors:
                    try:
                        donor_lat = float(donor['latitude'])
                        donor_lon = float(donor['longitude'])
                        distance = haversine(user_latitude, user_longitude, donor_lat, donor_lon)
                        donor['distance'] = round(distance, 2)
                    except ValueError:
                        donor['distance'] = None

                donors = sorted([d for d in donors if d['distance'] is not None], key=lambda x: x['distance'])

            return render_template('filterdonors.html', donors=donors)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred while fetching donors.', 'danger')
            return render_template('filterdonors.html', donors=[])
        finally:
            db.close()

    return render_template('filterdonors.html', donors=[])

if __name__ == '__main__':
    app.run(debug=True)
