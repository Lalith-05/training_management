from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from database.db_config import get_connection

selection_bp = Blueprint('selection', __name__)

# ----------------------------
# USER: Select a course
# ----------------------------
@selection_bp.route('/select_course/<course_id>', methods=['POST'])
def select_course(course_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('auth_bp.login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user's designation
    cursor.execute("SELECT designation FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if not user:
        conn.close()
        flash('User not found.')
        return redirect(url_for('course.view_courses'))

    designation = user['designation']

    # Mapping logic
    manager_designation = None
    if designation in ['E1', 'E2']:
        manager_designation = 'E7'
    elif designation in ['E3', 'E4']:
        manager_designation = 'E8'
    elif designation in ['E5', 'E6']:
        manager_designation = 'E9'

    if not manager_designation:
        conn.close()
        flash('No manager mapping found for your designation.')
        return redirect(url_for('course.view_courses'))

    # Get manager ID based on designation and role
    cursor.execute("""
        SELECT id FROM users 
        WHERE designation = %s AND role = 'manager'
        LIMIT 1
    """, (manager_designation,))
    manager = cursor.fetchone()

    if not manager:
        conn.close()
        flash(f'Manager with designation {manager_designation} not found.')
        return redirect(url_for('course.view_courses'))

    manager_id = manager['id']

    # Prevent duplicate selections
    cursor.execute("""
        SELECT 1 FROM course_selection 
        WHERE user_id = %s AND course_id = %s
    """, (session['user_id'], course_id))
    if cursor.fetchone():
        conn.close()
        flash('You have already selected this course.')
        return redirect(url_for('course.view_courses'))

    # Insert course selection request
    cursor.execute("""
        INSERT INTO course_selection (user_id, course_id, manager_id, status)
        VALUES (%s, %s, %s, 'pending')
    """, (session['user_id'], course_id, manager_id))
    conn.commit()
    conn.close()

    flash('Course selection submitted for approval.')
    return redirect(url_for('course.view_courses'))


# ----------------------------
# MANAGER: View pending approvals
# ----------------------------
@selection_bp.route('/approve_courses')
def approve_courses():
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth_bp.login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT cs.id, u.username, u.email, u.designation,
               c.name AS course_name, c.course_type, c.course_id
        FROM course_selection cs
        JOIN users u ON cs.user_id = u.id
        JOIN courses c ON cs.course_id = c.course_id
        WHERE cs.manager_id = %s AND cs.status = 'pending'
    """, (session['user_id'],))
    selections = cursor.fetchall()
    conn.close()

    return render_template('approve_courses.html', selections=selections)


# ----------------------------
# MANAGER: Handle approval or rejection
# ----------------------------
@selection_bp.route('/handle_request/<int:request_id>', methods=['POST'])
def handle_request(request_id):
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect(url_for('auth_bp.login'))

    action = request.form.get('action')
    reason = request.form.get('reason', '').strip()

    conn = get_connection()
    cursor = conn.cursor()

    if action == 'approve':
        cursor.execute("""
            UPDATE course_selection 
            SET status = 'approved', rejection_reason = NULL 
            WHERE id = %s
        """, (request_id,))
        flash('Request approved successfully.')

    elif action == 'reject':
        if not reason:
            flash('Rejection reason is required.')
            return redirect(url_for('selection.approve_courses'))
        cursor.execute("""
            UPDATE course_selection 
            SET status = 'rejected', rejection_reason = %s 
            WHERE id = %s
        """, (reason, request_id))
        flash('Request rejected successfully.')

    else:
        flash('Invalid action.')
        conn.close()
        return redirect(url_for('selection.approve_courses'))

    conn.commit()
    conn.close()
    return redirect(url_for('selection.approve_courses'))
