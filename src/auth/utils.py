from passlib.context import CryptContext
# token for email verification
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from pydantic import EmailStr
from config import Config

schemes = ["bcrypt"]
SECRET_KEY = Config.TOKEN_SECRET_KEY

pwd_context = CryptContext(schemes=schemes, deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# email verification 
token_algo = URLSafeTimedSerializer(secret_key=SECRET_KEY, salt="email-verification")

def generate_token(email: EmailStr) -> str:
    _token = token_algo.dumps(email)
    # .dumps() takes a Python object (here, the email) and serializes + signs it.
    return _token

def verify_token(token: str, max_age: int = 1800):
    try:
        email = token_algo.loads(token, max_age=max_age) # 1800 secs = 30 mins
        # .loads() verifies the token signature (checks it wasn’t tampered).
        return {"email": email, "check": True}
        
    except SignatureExpired:
        return None
    
    except BadSignature:
        return None
