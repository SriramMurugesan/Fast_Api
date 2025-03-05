from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Token) 
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Log the received credentials (email only for security)
    print(f"Login attempt for email: {user_credentials.username}")
    
    # Find user in database
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        print(f"User not found: {user_credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        print(f"Invalid password for user: {user_credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Successful login for user: {user_credentials.username}")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}