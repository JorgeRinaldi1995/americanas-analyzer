from flask import Flask, jsonify, request, session, redirect, url_for, flash
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# AWS Cognito User Pool details
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
REGION_NAME = os.getenv('REGION_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET') if the pool use a secret

# Set a secret key for Flask sessions
app.secret_key = SECRET_KEY  # Replace with a strong and unique secret key

# Initialize AWS Cognito client
client = boto3.client('cognito-idp', region_name=REGION_NAME)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
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
            {
                'Name': 'preferred_username',
                'Value': username
            },
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'name',
                'Value': name,
            },
            {
                'Name': 'family_name',
                'Value': family_name,
            }
        ]
    )

    return jsonify({'response': response})

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.get_json()
    username = data.get('username')
    confirm_code = data.get('confirm_code')

    response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        ConfirmationCode=confirm_code
    )
    
    return jsonify({'response': response})

@app.route('/api/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    response = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
    )

    access_token = response["AuthenticationResult"]["AccessToken"]

    response = client.get_user(
        AccessToken=access_token
    )
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 