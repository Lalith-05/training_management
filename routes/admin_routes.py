# admin_routes.py
from flask import Blueprint, render_template, session, redirect, request, flash
from database.db_config import get_connection

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/dashboard')

    return render_template('admin_dashboard.html', username=session['username'])


@admin_bp.route('/user_manager_map')
def user_manager_map():
    if session.get('role') != 'admin':
        return redirect('/dashboard')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.id AS manager_id, m.username AS manager_name, m.designation AS manager_designation,
               u.username AS user_name, u.designation AS user_designation, u.id AS user_id
        FROM users u
        JOIN users m ON u.manager_id = m.id
        WHERE u.role = 'user'
        ORDER BY m.id
    """)
    rows = cursor.fetchall()
    conn.close()

    # Group users under each manager
    manager_map = {}
    for row in rows:
        m_id = row['manager_id']
        if m_id not in manager_map:
            manager_map[m_id] = {
                'username': row['manager_name'],
                'designation': row['manager_designation'],
                'users': []
            }
        manager_map[m_id]['users'].append({
            'username': row['user_name'],
            'designation': row['user_designation'],
            'staff_no': row['user_id']  # using user ID as staff_no placeholder
        })

    managers = list(manager_map.values())

    return render_template('admin_user_manager_map.html', managers=managers)



@admin_bp.route('/reassign_user', methods=['GET', 'POST'])
def reassign_user():
    if session.get('role') != 'admin':
        return redirect('/dashboard')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        user_id = request.form['user_id']
        new_manager_id = request.form['manager_id']

        try:
            cursor.execute("UPDATE users SET manager_id = %s WHERE id = %s", (new_manager_id, user_id))
            conn.commit()
            flash("User reassigned successfully.")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}")

    cursor.execute("SELECT id, username FROM users WHERE role = 'user'")
    users = cursor.fetchall()

    cursor.execute("SELECT id, username FROM users WHERE role = 'manager'")
    managers = cursor.fetchall()

    conn.close()
    return render_template('admin_reassign_user.html', users=users, managers=managers)
