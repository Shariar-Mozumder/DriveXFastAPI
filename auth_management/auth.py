# auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
from sqlalchemy_orm.db_config import SessionLocal
from utils import hash_password, verify_password, create_access_token, send_otp_email,return_payload
from sqlalchemy_orm.models import Users, Otps,Auths  # Import the User and Otplog models
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
    try:
        # Check if username exists
        user = db.query(Users).filter(Users.Email == request.Email).first()
        if user and user.Status==1:
            return return_payload(status_code=400, message="Email already exists")
        elif user.Status==2:
            send_otp(user.Email,user.UserID,db)
            return return_payload(status_code=200, message="You are already registered, Please varify your account.")
        elif user.Status==3:
            return return_payload(status_code=400, message="Your account has been blocked.")

        # Hash the password
        hashed_password = hash_password(request.Password)

        # Create new user
        new_user = Users(FirstName=request.FirstName,LastName=request.LastName, RoleID=request.RoleID,
                        Email=request.Email,Gender=request.Gender, PhoneNumber=request.PhoneNumber,
                            Password=hashed_password, Status=2,CreateDate=datetime.utcnow(),AddressID=request.AddressID)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        if new_user.UserID !=None:
            send_otp(new_user.Email,new_user.UserID,db)
        
        return return_payload(200, "User registered successfully, Please verify account with OTP.")

    except Exception as e:
        return return_payload(500,"Error: "+str(e))

        

# Send OTP
def send_otp(email, userid,db: Session):
    # db = next(get_db)
    # Generate 4-digit OTP
    otp = random.randint(1000, 9999)
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes

    # # Check if an OTP was sent recently
    # otp_entry = db.query(Otps).filter(Otplog.Email == request.email, Otplog.Verified == False).first()
    # if otp_entry:
    #     raise HTTPException(status_code=400, detail="OTP already sent. Please wait for the previous one to expire.")

    # Store OTP in the database
    otp_log = Otps(Email=email,UserID=userid, OtpCode=otp, OtpExpiredTime=otp_expiry)
    db.add(otp_log)
    db.commit()
    db.refresh(otp_log)

    # Send OTP to email
    send_otp_email(email, str(otp))

    return {"msg": "OTP sent to your email"}

# Verify OTP Endpoint
@router.post("/verify_otp")
async def verify_otp(request: VerifyOtpRequest, db: Session = Depends(get_db)):
    try:
        otp_entry = db.query(Otps).filter(Otps.Email == request.Email).order_by(Otps.OtpID.desc()).first()
        current_time=datetime.utcnow()
        if not otp_entry:
            return return_payload(400,"No OTP sent to this email")

        # Check if OTP is expired
        if current_time > otp_entry.OtpExpiredTime:
            return return_payload(400, "OTP expired")

        if otp_entry.OtpCode != request.OtpCode:
            return return_payload(400, "Invalid OTP")

        # Mark OTP as verified
        user=db.query(Users).filter(Users.UserID==otp_entry.UserID).first()
        if user:
            user.Status=1
            db.commit()
        return return_payload(200,"User varified Successfully.")
    
    except Exception as e:
        return return_payload(500,"Error: "+str(e))

# Login Endpoint
@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Find the user by username
    user = db.query(Users).filter(Users.Email == request.Email).first()
    if not user or not verify_password(request.Password, user.Password):
        return return_payload(400, "Invalid credentials")
    
    #if old user
    oldAuth=db.query(Auths).filter(Auths.UserID==user.UserID).first()
    if oldAuth and oldAuth.TokenExpiredDate>datetime.utcnow():
        token_expiredate=datetime.utcnow() + timedelta(days=1)
        oldAuth.TokenExpiredDate=token_expiredate
        oldAuth.LastLoginDate=datetime.utcnow()
        db.commit()
        return return_payload(200,"Login Successfull",{"Token: "+oldAuth.Token})

    # Create an access token
    access_token,expiretime = create_access_token({"sub": user.Email})
    auth=Auths(UserID=user.UserID,Token=access_token,LastLoginDate=datetime.utcnow(),
               CreatedDate=datetime.utcnow(),RoleID=user.RoleID,TokenExpiredDate=expiretime)
    db.add(auth)
    db.commit()
    db.refresh(auth)
    
    return return_payload(200,"Login Successfull",{"Token: "+access_token})