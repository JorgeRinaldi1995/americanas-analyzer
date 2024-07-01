import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Replace with a strong and unique secret key
    # Add other configuration settings as needed
