TRAINING_MANAGEMENT_SYSTEM

A brief description of what this project does and who it's for
The Training Management System is a role-based web platform that streamlines the process of employee training in an organization. It allows users to view and select courses, submit feedback, and get approval from their assigned managers. Managers can approve or reject course requests and review feedback from users. An admin user has advanced control over the course listings and user-manager assignments. The system is built using Flask, MySQL, HTML, CSS, and JavaScript.

It is specifically designed for a structured enterprise training environment where approval workflows, designation-based access, and feedback mechanisms are essential for scalable and efficient training management.



## Features

🔐 User authentication and role-based access (User / Manager / Admin)

📚 Categorized course listings (Technical, Quality, Certificate, General)

📨 Course selection with approval workflows based on designation level

🗂 Admin panel to manage users, courses, and manager assignments

📝 Feedback module for users and managerial review

📊 Dashboard views customized per role

📤 Email notifications (optional)

🚫 Rejection handling with mandatory comments




## Prerequistes
Python 3.8+

MySQL Server (with Workbench optional)

pip
## Roadmap

📦 MVP (Minimum Viable Product)
User authentication system (User / Manager / Admin roles)

Course display by category

Course selection and approval based on designation level

Basic admin panel to manage courses and users

User feedback submission

Manager review of feedback

🎯 Phase 2: Core Enhancements
Role-based dashboards with personalized views

Manager reassignments by admin

Course deletion and confirmation flow

Mandatory rejection reasons for managers

✨ Phase 3: UI & UX Improvements
Responsive UI for all devices

JavaScript form validations

Dashboard cards and improved layout

Prevent resubmission and improve form interactions

📨 Phase 4: Optional Features
Email notifications (on approval, rejection, feedback)

Export course/feedback data (CSV, PDF)

Pagination and search for large course catalogs

🚀 Phase 5: Deployment
Prepare for production with .env and secure configs

Deploy using Flask-compatible platforms (Heroku, Render, etc.)

Remote MySQL or cloud database integration

🔮 Future Ideas
Course progress tracking

Certificate generation after course completion

Manager analytics dashboard

Excel course import (bulk upload)


## Installation

# 1. Clone the repository
git clone https://github.com/your-username/training_management.git
cd training_management

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Setup MySQL
- Create database 'training_db'
- Run schema.sql to set up tables

# 4. Run the Flask app
python app.py
    
## Usage
Register as a User or Manager.

Login to your dashboard (based on role).

1.Users can:

    View courses by category

    Select applicable courses

    Submit feedback after course completion

2.Managers can:

    View requests from users

    Approve or reject requests

    View and respond to feedback

Admin can:

    Add or delete courses

    Assign/reassign managers to users

    Access full platform control
## Badges

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)



## Authors

- [@Lalith_kishore](https://www.github.com/Lalith-05) - full stack developer

