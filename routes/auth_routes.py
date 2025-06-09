from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_config import get_connection
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        username = request.form['username'].strip()
        staff_no = request.form['staff_no'].strip()
        email = request.form['email'].strip()
        department = request.form['department'].strip()
        designation = request.form['designation'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Basic validations
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect('/register')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format")
            return redirect('/register')
        if len(username) < 8 or len(username) > 15:
            flash("Username must be between 8 and 15 characters")
            return redirect('/register')

        role = 'user' if designation in ['E1', 'E2', 'E3', 'E4', 'E5', 'E6'] else 'manager'
        password_hash = generate_password_hash(password)

        try:
            cursor.execute("""
                INSERT INTO users (username, staff_no, email, department, designation, password_hash, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, staff_no, email, department, designation, password_hash, role))
            db.commit()
            flash("Registration successful.")
            return redirect('/login')
        except Exception as e:
            flash(f"Error: {e}")
            return redirect('/register')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        staff_no = request.form['staff_no'].strip()
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE staff_no = %s", (staff_no,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['designation'] = user['designation']
            flash("Login successful.")
            return redirect('/dashboard')

        flash("Invalid credentials")
        return redirect('/login')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect('/login')

