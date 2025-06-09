from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from database.db_config import get_connection
from werkzeug.security import check_password_hash

course_bp = Blueprint('course_bp', __name__)

# View courses (accessible by both users and managers)
@course_bp.route('/courses')
def view_courses():
    if 'user_id' not in session:
        return redirect('/login')

    selected_type = request.args.get('type')
    query = "SELECT * FROM courses"
    values = ()

    if selected_type:
        query += " WHERE course_type = %s"
        values = (selected_type,)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, values)
    courses = cursor.fetchall()
    conn.close()

    return render_template('courses.html', courses=courses, selected_type=selected_type)


# MANAGER: Add course
@course_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'role' not in session or session['role'] != 'manager':
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        duration = request.form['duration']
        provider = request.form['provider']
        levels = request.form['levels']
        description = request.form['description']
        course_type = request.form['course_type']

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO courses 
                (name, duration, training_provider, applicable_levels, description, course_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, duration, provider, levels, description, course_type))
            conn.commit()
            flash('Course added successfully!')
        except Exception as e:
            conn.rollback()
            flash(f'Error while adding course: {e}')
        finally:
            conn.close()

        return redirect(url_for('course_bp.view_courses'))

    return render_template('add_course.html')


# MANAGER: Delete course with password confirmation
@course_bp.route('/delete_course/<course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    if 'role' not in session or session['role'] != 'manager':
        return redirect('/login')

    if request.method == 'POST':
        password = request.form['password']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT password_hash FROM users WHERE id = %s", (session['user_id'],))
        manager = cursor.fetchone()

        if manager and check_password_hash(manager['password_hash'], password):
            try:
                cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
                conn.commit()
                flash('Course deleted successfully.')
            except Exception as e:
                conn.rollback()
                flash(f'Error deleting course: {e}')
        else:
            flash('Incorrect password. Cannot delete course.')

        conn.close()
        return redirect(url_for('course_bp.view_courses'))

    return render_template('confirm_delete.html', course_id=course_id)
