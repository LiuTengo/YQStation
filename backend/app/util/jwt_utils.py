import jwt
from datetime import UTC, datetime, timedelta
SECRET_KEY = "YQStation_signin_system_secret_key"

ALGORITHM = "HS256"

def create_token(student_id: str):

    payload = {
        "student_id": student_id,
        "exp": datetime.now(UTC) + timedelta(days=7)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["student_id"]
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")