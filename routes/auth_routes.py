from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_config import get_connection
import re

auth_bp = Blueprint('auth', __name__)

# 🧠 Mapping: user designation -> eligible manager designation
designation_to_manager = {
    'E1': 'E7', 'E2': 'E7',
    'E3': 'E8', 'E4': 'E8',
    'E5': 'E9', 'E6': 'E9',
}

# 🔁 Helper: get manager with fewest users
def get_least_loaded_manager(user_designation):
    manager_designation = designation_to_manager.get(user_designation)
    if not manager_designation:
        return None

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.id AS manager_id, COUNT(usr.id) AS user_count
        FROM users u
        LEFT JOIN users usr ON usr.manager_id = u.id
        WHERE u.designation = %s AND u.role = 'manager'
        GROUP BY u.id
        ORDER BY user_count ASC
        LIMIT 1
    """, (manager_designation,))

    result = cursor.fetchone()
    cursor.close()
    db.close()

    return result['manager_id'] if result else None


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        username = request.form['username'].strip()
        staff_no = request.form['staff_no'].strip()
        email = request.form['email'].strip()
        department = request.form['department'].strip()
        designation = request.form['designation'].strip().upper()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect('/register')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format")
            return redirect('/register')
        if len(username) < 8 or len(username) > 15:
            flash("Username must be between 8 and 15 characters")
            return redirect('/register')

        # Determine role
        if designation in ['E1', 'E2', 'E3', 'E4', 'E5', 'E6']:
            role = 'user'
        elif designation in ['E7', 'E8', 'E9']:
            role = 'manager'
        else:
            flash("Invalid designation level.")
            return redirect('/register')

        # Block admin registration
        if role == 'admin':
            flash("Admin registration is not allowed.")
            return redirect('/register')

        # Hash password
        password_hash = generate_password_hash(password)

        # 🔁 Assign least-loaded manager for user
        manager_id = None
        if role == 'user':
            manager_id = get_least_loaded_manager(designation)
            if not manager_id:
                flash("No eligible manager available for your designation.")
                return redirect('/register')

        # Insert user
        try:
            cursor.execute("""
                INSERT INTO users (username, staff_no, email, department, designation, password_hash, role, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, staff_no, email, department, designation, password_hash, role, manager_id))
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

            # Redirect based on role
            return redirect('/dashboard') if user['role'] != 'admin' else redirect('/admin/dashboard')

        flash("Invalid credentials")
        return redirect('/login')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect('/login')
