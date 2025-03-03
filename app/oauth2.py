from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, models
from app.database import get_db
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        print(f"Verifying token: {token[:10]}...")  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")  
        id: int = payload.get("user_id")
        print(f"Extracted user_id: {id}")  
        if id is None:
            print("No user_id found in token")
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        print(f"Created TokenData: {token_data}")  
    except JWTError as e:
        print(f"JWT Error: {str(e)}")  
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    print(f"Getting current user with token: {token[:10]}...")  
    token_data = verify_access_token(token, credentials_exception)
    print(f"Token data received: {token_data}")  
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    print(f"User found: {user}")  
    
    if user is None:
        print("No user found in database")
        raise credentials_exception
    
    return user