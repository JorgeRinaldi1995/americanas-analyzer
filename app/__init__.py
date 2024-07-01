from flask import Flask
from dotenv import load_dotenv
import boto3
import os

# Load environment variables from .env file
load_dotenv()

# Initialize AWS Cognito client
client = boto3.client('cognito-idp', region_name='us-east-1')

# AWS Cognito User Pool details
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ovolactose123'  # Replace with a strong and unique secret key
    
    with app.app_context():
        # Register Blueprints
        from app.auth.routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api')
        
    return app