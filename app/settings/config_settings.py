import logging
import os

import dotenv
from pathlib import Path

from fastapi.security import OAuth2PasswordBearer

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger()


if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# bd_settings
host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
port = os.environ["PORT"]
db_url = os.environ["DB_URL"]


# token configuration
token_secret_key = os.environ["SECRET_KEY"]
algorithm = os.environ["ALGORITHM"]
access_token_expire_minutes = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
refresh_token_expire_days = os.environ["REFRESH_TOKEN_EXPIRE_DAYS"]
TOKEN_TYPE: str = "Bearer"
REFRESH_TOKEN_JWT_SUBJECT: str = 'refresh'
ACCESS_TOKEN_JWT_SUBJECT: str = 'access'


# email configuration
email_host_user = os.environ["EMAIL_HOST_USER"]
email_host_password = os.environ["EMAIL_HOST_PASSWORD"]
email_host = os.environ["EMAIL_HOST"]
