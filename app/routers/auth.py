from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Log the received credentials (email only for security)
    print(f"Login attempt for email: {user_credentials.email}")
    
    # Find user in database
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        print(f"User not found: {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        print(f"Invalid password for user: {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Successful login for user: {user_credentials.email}")
    return {"message": "Login Successful"}