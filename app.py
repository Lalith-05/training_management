from flask import Flask , render_template
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.selection_routes import selection_bp
from routes.course_routes import course_bp
from routes.admin_routes import admin_bp
from routes.feedback_routes import feedback_bp
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(course_bp, url_prefix='/course')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(selection_bp, url_prefix='/selection')
app.register_blueprint(admin_bp)
app.register_blueprint(feedback_bp, url_prefix='/feedback')

@app.route('/')
def home():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)
