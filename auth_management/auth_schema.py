# schemas.py
from pydantic import BaseModel
from typing import Optional

# Pydantic model for user registration
class RegisterUserRequest(BaseModel):
    FirstName: str
    LastName: str
    PhoneNumber: str
    Email: str
    Password: str

# Pydantic model for login
class LoginRequest(BaseModel):
    Email: str
    Password: str

# Pydantic model for sending OTP
class SendOtpRequest(BaseModel):
    Email: str

# Pydantic model for verifying OTP
class VerifyOtpRequest(BaseModel):
    Email: str
    OtpCode: int

# Pydantic model for creating a new user after OTP verification
class CreateUserRequest(BaseModel):
    FirstName: str
    LastName: str
    PhoneNumber: str
    Email: str
    Password: str
