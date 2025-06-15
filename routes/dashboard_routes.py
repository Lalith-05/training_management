# dashboard_routes.py
from flask import Blueprint, render_template, session, redirect, request
from database.db_config import get_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    # Redirect based on role
    role = session.get('role', 'user')
    if role == 'admin':
        return redirect('/admin/dashboard')
    return render_template('dashboard.html', username=session['username'], role=role)


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


@dashboard_bp.route('/my_courses')
def my_courses():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect('/dashboard')

    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT cs.status, cs.rejection_reason AS reason, c.name, c.course_type, c.course_id
        FROM course_selection cs
        JOIN courses c ON cs.course_id = c.course_id
        WHERE cs.user_id = %s
    """, (user_id,))

    courses = cursor.fetchall()

    for course in courses:
        cursor.execute("""
            SELECT manager_comments, allow_to_continue
            FROM feedback
            WHERE user_id = %s AND course_id = %s
            LIMIT 1
        """, (user_id, course['course_id']))
        fb = cursor.fetchone()

        if fb:
            course['feedback_submitted'] = True
            course['manager_comments'] = fb['manager_comments']
            course['allow_to_continue'] = fb['allow_to_continue']
        else:
            course['feedback_submitted'] = False
            course['manager_comments'] = None
            course['allow_to_continue'] = None

    conn.close()

    return render_template('my_courses.html', my_courses=courses)
