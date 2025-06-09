from flask import Blueprint, render_template, session, redirect, request
from database.db_config import get_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        username=session['username'],
        role=session.get('role', 'user')  # default to 'user' if role not set
    )

@dashboard_bp.route('/courses')
def courses():
    if 'username' not in session:
        return redirect('/login')

    selected_type = request.args.get('type', '')
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if selected_type:
        cursor.execute("SELECT * FROM courses WHERE course_type = %s", (selected_type,))
    else:
        cursor.execute("SELECT * FROM courses")

    courses = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('courses.html', courses=courses, selected_type=selected_type)

@dashboard_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if session.get('role') != 'manager':
        return redirect('/dashboard')
    return render_template('add_course.html')  # Ensure this template exists

@dashboard_bp.route('/approve_courses')
def approve_courses():
    if session.get('role') != 'manager':
        return redirect('/dashboard')
    return render_template('approve_courses.html')  # Ensure this template exists

@dashboard_bp.route('/my_courses')
def my_courses():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect('/dashboard')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch selected courses for the logged-in user
    cursor.execute("""
    SELECT cs.status, cs.rejection_reason AS reason, c.name, c.course_type, c.course_id
    FROM course_selection cs
    JOIN courses c ON cs.course_id = c.course_id
    WHERE cs.user_id = %s
""", (session['user_id'],))


    courses = cursor.fetchall()
    conn.close()

    return render_template('my_courses.html', my_courses=courses)

