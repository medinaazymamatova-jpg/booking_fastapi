# import secrets
#
# print(secrets.token_hex(64))

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

ACCESS_TOKEN_LIFETIME = 15
REFRESH_TOKEN_LIFETIME = 60
ALGORITHM = 'HS256'