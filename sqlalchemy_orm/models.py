# models.py
from datetime import datetime
import enum
from sqlalchemy import Enum, create_engine, Column, Integer, String, DateTime, Boolean,ForeignKey,Text,Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=True)
    Password = Column(String(50), nullable=False)
    ImageID = Column(Integer, ForeignKey("Images.ImageID"), nullable=True)
    RoleID = Column(Integer, nullable=True)
    Email = Column(String(50), nullable=False)
    Gender = Column(String(10), nullable=True)
    BirthDate = Column(DateTime, nullable=True)
    PhoneNumber = Column(String(50), nullable=False)
    Status = Column(SmallInteger, nullable=True)
    CreateDate = Column(DateTime, nullable=True)
    AddressID = Column(Integer, ForeignKey("Address.AddressID"), nullable=True)

    # Relationship
    address = relationship("Address", back_populates="users")
    images = relationship("Images", back_populates="users")
    auths = relationship("Auths", back_populates="users")
    

class Address(Base):
    __tablename__ = "Address"
    
    AddressID = Column(Integer, primary_key=True, autoincrement=True)
    AddressLine1 = Column(String(50), nullable=True)
    AddressLine2 = Column(String(50), nullable=True)
    City = Column(String(50), nullable=False)
    PostalCode = Column(String(50), nullable=True)
    Country = Column(String(50), nullable=True)
    Telephone = Column(String(50), nullable=True)
    Mobile = Column(String(50), nullable=True)
    Status = Column(SmallInteger, nullable=True)
    isActive = Column(Boolean, nullable=True)
    Lattitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)
    AddressType = Column(SmallInteger, nullable=True)
    CreatedDate = Column(DateTime, nullable=True)
    
    # Back-reference to Users
    users = relationship("Users", back_populates="address")

class Auths(Base):
    __tablename__ = "Auths"
    
    AuthID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    Token = Column(String(255), nullable=False)
    LastLoginDate = Column(DateTime, nullable=True)
    CreatedDate = Column(DateTime, nullable=True)
    RoleID = Column(Integer, nullable=True)
    
    # Relationship with Users
    users = relationship("Users", back_populates="auths")

class Otps(Base):
    __tablename__ = "Otps"
    
    OtpID = Column(Integer, primary_key=True, autoincrement=True)
    OtpCode = Column(String(50), nullable=False)
    OtpExpiredTime = Column(DateTime, nullable=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    
    # Relationship with Users
    # user = relationship("Users", back_populates="otps")

class Images(Base):
    __tablename__="Images"

    ImageID=Column(Integer, primary_key=True, autoincrement=True)
    ImageFile=Column(String(max), nullable=True)

    users = relationship("Users", back_populates="images")