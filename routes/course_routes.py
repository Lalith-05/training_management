from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from database.db_config import get_connection
from werkzeug.security import check_password_hash

course_bp = Blueprint('course', __name__)

# View courses (accessible by all roles)
@course_bp.route('/view_courses')
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
    all_courses = cursor.fetchall()
    conn.close()

    # For users: filter based on applicable_levels range
    if session.get('role') == 'user':
        user_designation = session.get('designation')  # e.g., 'E3'

        def is_designation_in_range(range_str, user_designation):
            try:
                start, end = range_str.split('-')
                return start <= user_designation <= end
            except ValueError:
                return False

        filtered_courses = [
            course for course in all_courses
            if is_designation_in_range(course['applicable_levels'], user_designation)
        ]
    else:
        # For managers/admins, show all
        filtered_courses = all_courses

    return render_template('courses.html', courses=filtered_courses, selected_type=selected_type)


# ADMIN: Add course
@course_bp.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied. Only admin can add courses.")
        return redirect('/dashboard')

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

        return redirect(url_for('course.courses'))

    return render_template('add_course.html')


# Updated DELETE COURSE route with password confirmation and delete interface
@course_bp.route('/delete_course', methods=['GET', 'POST'])
def delete_course():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied. Only admin can delete courses.")
        return redirect('/dashboard')

    if request.method == 'POST':
        password = request.form['password']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT password_hash FROM users WHERE id = %s", (session['user_id'],))
        admin = cursor.fetchone()

        if admin and check_password_hash(admin['password_hash'], password):
            # Store password check success in session
            session['admin_verified'] = True
        else:
            flash('Incorrect password. Cannot proceed.')
            return redirect(url_for('course.delete_course'))

        conn.close()

    # Step 2: Show course list only if verified
    if session.get('admin_verified'):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.close()
        return render_template('delete_course_list.html', courses=courses)

    return render_template('confirm_delete.html')

@course_bp.route('/delete_specific_course/<course_id>', methods=['POST'])
def delete_specific_course(course_id):
    if 'role' not in session or session['role'] != 'admin' or not session.get('admin_verified'):
        flash("Unauthorized access.")
        return redirect('/dashboard')

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
        conn.commit()
        flash(f"Course {course_id} deleted.")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting course: {e}")
    conn.close()
    return redirect(url_for('course.delete_course'))

