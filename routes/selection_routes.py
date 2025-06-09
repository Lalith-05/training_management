from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from database.db_config import get_connection

selection_bp = Blueprint('selection_bp', __name__)

# User: Select a course
@selection_bp.route('/select_course/<course_id>', methods=['POST'])
def select_course(course_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('auth_bp.login'))  # Assuming auth_bp handles login

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user designation
    cursor.execute("SELECT designation FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user:
        conn.close()
        flash('User not found.')
        return redirect(url_for('dashboard.courses'))

    designation = user['designation']

    # Determine manager level mapping
    mapping = {
        'E1': 'E6', 'E2': 'E6',
        'E3': 'E7', 'E4': 'E7',
        'E5': 'E8', 'E6': 'E8'
    }
    manager_level = mapping.get(designation)
    if not manager_level:
        conn.close()
        flash('No approval manager found for your level.')
        return redirect(url_for('dashboard.courses'))

    # Get manager ID
    cursor.execute("SELECT id FROM users WHERE designation = %s AND role = 'manager' LIMIT 1", (manager_level,))
    manager = cursor.fetchone()

    if not manager:
        conn.close()
        flash('Manager not found for approval.')
        return redirect(url_for('dashboard.courses'))

    manager_id = manager['id']

    # Check if already selected
    cursor.execute("SELECT * FROM course_selection WHERE user_id = %s AND course_id = %s", (session['user_id'], course_id))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        flash('You have already selected this course.')
        return redirect(url_for('dashboard.courses'))

    # Insert new selection
    cursor.execute(
        "INSERT INTO course_selection (user_id, course_id, manager_id, status) VALUES (%s, %s, %s, 'pending')",
        (session['user_id'], course_id, manager_id)
    )
    conn.commit()
    conn.close()
    flash('Course selection submitted for approval.')
    return redirect(url_for('dashboard.courses'))


# Manager: View course selection requests
@selection_bp.route('/approve_courses')
def approve_courses():
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth_bp.login'))  # Assuming auth_bp handles login

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT cs.id, u.username, u.email, u.designation, c.name AS course_name, 
               c.course_type, c.course_id
        FROM course_selection cs
        JOIN users u ON cs.user_id = u.id
        JOIN courses c ON cs.course_id = c.course_id
        WHERE cs.manager_id = %s AND cs.status = 'pending'
    """, (session['user_id'],))
    selections = cursor.fetchall()
    conn.close()

    return render_template('approve_courses.html', selections=selections)


# Manager: Approve or reject a course request
@selection_bp.route('/handle/<int:request_id>', methods=['POST'])
def handle_request(request_id):
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth_bp.login'))  # Assuming auth_bp handles login

    action = request.form['action']
    reason = request.form.get('reason', '')

    conn = get_connection()
    cursor = conn.cursor()

    if action == 'approve':
        cursor.execute("UPDATE course_selection SET status = 'approved', rejection_reason = NULL WHERE id = %s", (request_id,))
    elif action == 'reject':
        cursor.execute("UPDATE course_selection SET status = 'rejected', rejection_reason = %s WHERE id = %s", (reason, request_id))

    conn.commit()
    conn.close()
    flash(f'Request {action}d successfully.')
    return redirect(url_for('selection_bp.approve_courses'))
