from flask import Blueprint, render_template, request
from ..controllers.auth_controllers import register_user, verify_email, user_auth, show_profile, user_logout
from app.auth.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register_user()
        
    return render_template('auth/register.html', title='Register')

@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        return verify_email()
    return render_template('auth/verify.html', title='Verify')

@auth_bp.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return user_auth()
    return render_template('auth/login.html', title='Login')


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        return user_logout()
    return render_template('auth/logout.html', title='Logout')

@auth_bp.route('/profile')
@login_required
def profile():
    return show_profile()