from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from database.db_config import get_connection
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/submit_feedback/<int:course_id>', methods=['GET', 'POST'])
def submit_feedback(course_id):
    if 'user_id' not in session or session.get('role') != 'user':
        flash("Access denied.")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Check if feedback already exists
    cursor.execute("SELECT * FROM feedback WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    existing_feedback = cursor.fetchone()

    if existing_feedback:
        flash("You have already submitted feedback for this course.")
        conn.close()
        return redirect(url_for('dashboard.my_courses'))

    # Get course info for rendering
    cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()

    # Get user info for display
    cursor.execute("SELECT username, staff_no, department, designation, manager_id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        training_date = request.form.get('training_date')
        course_helpful_raw = request.form.get('course_helpful')
        course_helpful = 1 if course_helpful_raw == 'yes' else 0  # ✅ convert to int

        course_rating = request.form.get('course_rating')
        trainer_name = request.form.get('trainer_name')
        trainer_rating = request.form.get('trainer_rating')
        course_review = request.form.get('course_review')
        trainer_review = request.form.get('trainer_review')
        understood_concepts = request.form.get('understood_concepts')
        improvements = request.form.get('improvements')

        # ✅ Insert feedback into DB
        cursor.execute("""
            INSERT INTO feedback (
                user_id, course_id, training_date, course_helpful, course_rating,
                trainer_name, trainer_rating, course_review, trainer_review,
                understood_concepts, improvements, submitted_at, manager_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """, (
            user_id, course_id, training_date, course_helpful, course_rating,
            trainer_name, trainer_rating, course_review, trainer_review,
            understood_concepts, improvements, user['manager_id']
        ))

        conn.commit()
        conn.close()
        flash("Feedback submitted successfully.")
        return redirect(url_for('dashboard.my_courses'))

    conn.close()
    return render_template('feedback_form.html', course=course, user=user)


@feedback_bp.route('/view_feedbacks')
def view_feedbacks():
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect('/dashboard')

    manager_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.*, c.name AS course_name, c.course_id, u.username, u.staff_no, u.designation
        FROM feedback f
        JOIN courses c ON f.course_id = c.course_id
        JOIN users u ON f.user_id = u.id
        WHERE u.manager_id = %s AND f.manager_reviewed = FALSE
    """, (manager_id,))

    feedbacks = cursor.fetchall()
    conn.close()

    return render_template('manager_feedbacks.html', feedbacks=feedbacks)


@feedback_bp.route('/update_feedback/<int:feedback_id>', methods=['POST'])
def update_feedback(feedback_id):
    if 'user_id' not in session or session.get('role') != 'manager':
        return redirect('/dashboard')

    manager_comments = request.form.get('manager_comments')
    allow_to_continue = request.form.get('allow_to_continue')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE feedback
        SET manager_comments = %s,
            allow_to_continue = %s,
            manager_reviewed = TRUE
        WHERE id = %s
    """, (manager_comments, allow_to_continue, feedback_id))

    conn.commit()
    conn.close()
    return redirect(url_for('feedback.view_feedbacks'))
