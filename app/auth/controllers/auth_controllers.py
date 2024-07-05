from flask import request, render_template, session, redirect, url_for
from app import client, CLIENT_ID

def register_user():
    
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

def verify_email():
    
    data = request.form
    username = data.get('username')
    confirm_code = data.get('confirm_code')

    response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        ConfirmationCode=confirm_code
    )
    
    return redirect(url_for('auth.login'))
    

def user_auth():
    
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
    
def user_logout():
    
    access_token = session.get('access_token')

    if access_token:
                try:
                    client.global_sign_out(
                        AccessToken=access_token
                    )
                except client.exceptions.NotAuthorizedException:
                    pass  # Handle the exception as needed
    session.clear()
    return redirect(url_for('auth.login'))
    

def show_profile():
    user_attributes = session.get('user', [])
    return render_template('auth/profile.html', title='Profile', user_attributes=user_attributes)