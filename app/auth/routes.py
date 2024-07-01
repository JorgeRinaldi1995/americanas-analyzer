from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from app import client, CLIENT_ID
from app.auth.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        name = data.get('name')
        family_name = data.get('family_name')
        email = data.get('email')
        password = data.get('password')

        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                {'Name': 'preferred_username', 'Value': username},
                {'Name': 'email', 'Value': email},
                {'Name': 'name', 'Value': name},
                {'Name': 'family_name', 'Value': family_name},
            ]
        )

        return redirect(url_for('auth.verify'))
    return render_template('auth/register.html', title='Register')

@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        confirm_code = data.get('confirm_code')

        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=confirm_code
        )
        
        return redirect(url_for('auth.login'))
    return render_template('auth/verify.html', title='Verify')

@auth_bp.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': password},
        )

        access_token = response["AuthenticationResult"]["AccessToken"]

        user_response = client.get_user(AccessToken=access_token)

        session['user'] = user_response['UserAttributes']
        session['access_token'] = access_token

        return redirect(url_for('auth.profile'))
    return render_template('auth/login.html', title='Login')

@auth_bp.route('/profile')
@login_required
def profile():
    user_attributes = session.get('user', [])
    return render_template('auth/profile.html', title='Profile', user_attributes=user_attributes)