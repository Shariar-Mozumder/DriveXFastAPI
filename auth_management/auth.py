# auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from sqlalchemy_orm.db_config import SessionLocal
from utils import hash_password, verify_password, create_access_token, send_otp_email,return_payload
from sqlalchemy_orm.models import Users, Otps  # Import the User and Otplog models
from .auth_schema import RegisterUserRequest, LoginRequest, SendOtpRequest, VerifyOtpRequest, CreateUserRequest
from jose import JWTError, jwt
from typing import List
# Secret key for encoding and decoding JWT tokens
SECRET_KEY = "your_secret_key"  # Replace with your secret key
ALGORITHM = "HS256"

# OAuth2 password bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register Endpoint
@router.post("/register")
async def register(request: RegisterUserRequest, db: Session = Depends(get_db)):
    # Check if username exists
    user = db.query(Users).filter(Users.Email == request.Email).first()
    if user:
        return return_payload(status_code=400, message="Email already exists")

    # Hash the password
    # hashed_password = hash_password(request.Password)

    # Create new user
    new_user = Users(FirstName=request.FirstName,LastName=request.LastName, Email=request.Email, PhoneNumber=request.PhoneNumber, Password=request.Password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.UserID}