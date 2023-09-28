from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import schemas, models

SECRET_KEY = "f2226d7ef6fa5478d6b74ce93c3ca0616009db1f42bb89c98df45e75f833419a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(username=username)
        
        return token_data
    except JWTError:
        raise credentials_exception