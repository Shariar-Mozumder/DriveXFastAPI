from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),expire

# Function to send OTP email
def send_otp_email(email: str, otp: str):
    from_email = "shmozumder2@gmail.com"  # Replace with actual email
    from_password = "bavynppryhpoktub"  # Replace with your email password
    
    to_email = email
    
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    # Create message
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Replace with your SMTP server details
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, message.as_string())

def return_payload(status_code,payload=None, message=None):
    payload_obj={
        'code': status_code,
        'message': message,
        'payload': payload
    }
    return payload_obj