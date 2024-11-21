# models.py
import enum
from sqlalchemy import Enum, create_engine, Column, Integer, BigInteger, String, DateTime, Boolean,ForeignKey,Text,Float,SmallInteger
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
    TokenExpiredDate=Column(DateTime, nullable=True)

    
    # Relationship with Users
    users = relationship("Users", back_populates="auths")

class Otps(Base):
    __tablename__ = "Otps"
    
    OtpID = Column(Integer, primary_key=True, autoincrement=True)
    OtpCode = Column(String(50), nullable=False)
    OtpExpiredTime = Column(DateTime, nullable=True)
    UserID = Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    Email=Column(String(50),nullable=True)
    CreatedTime=Column(DateTime, nullable=True)
    # Relationship with Users
    # user = relationship("Users", back_populates="otps")

class Images(Base):
    __tablename__="Images"

    ImageID=Column(BigInteger, primary_key=True, autoincrement=True)
    ImageFile1=Column(Text, nullable=True)
    ImageFile2=Column(Text, nullable=True)
    ImageFile3=Column(Text, nullable=True)
    ImageFile4=Column(Text, nullable=True)
    ImageFile5=Column(Text, nullable=True)
    ProductID = Column(BigInteger, ForeignKey("Products.ProductID"), nullable=True)

    # users = relationship("Users", back_populates="images")

class Categories(Base):
    __tablename__="Categories"

    CategoryID=Column(Integer, primary_key=True, autoincrement=True)
    CategoryName=Column(String(50),nullable=False)
    CategoryType=Column(String(50),nullable=True)
    CreateDate=Column(DateTime, nullable=True)
    Status=Column(Integer,nullable=True)

class Products(Base):
    __tablename__="Products"

    ProductID=Column(BigInteger, primary_key=True, autoincrement=True)
    UserID=Column(Integer, ForeignKey("Users.UserID"), nullable=False)
    CategoryID=Column(Integer, ForeignKey("Categories.CategoryID"), nullable=False)
    # ImageID=Column(BigInteger, ForeignKey("Images.ImageID"), nullable=True)
    Name=Column(String(50),nullable=True)
    Description= Column(Text,nullable=True)
    Specifications =Column(Text,nullable=True)
    Price =Column(Float,nullable=False)
    Quantity =Column(Integer,nullable=True)
    IsAuction =Column(Boolean,nullable=True)
    Status =Column(Integer,nullable=True)
    CreatedDate =Column(DateTime,nullable=True)
    CreatedBy = Column(Integer,nullable=True)

    # images = relationship("Images", back_populates="products")