import os


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
ALGORITHM = "HS256"
access_token_jwt_subject = "access"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = os.getenv('SECRET_KEY')
