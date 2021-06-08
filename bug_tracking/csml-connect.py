import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('MY_ENV_VAR')
API_SECRET = os.getenv('MY_ENV_VAR')


timestamp = str(int(time.time()))
x_api_key = API_KEY + "|" + timestamp

signature = hmac.new(
    str.encode(API_SECRET),
    x_api_key.encode('utf8'),
    digestmod=hashlib.sha256
).hexdigest()
x_api_signature = "sha256=" + signature
