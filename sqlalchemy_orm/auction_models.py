# models.py
import enum
from sqlalchemy import Enum, create_engine, Column, Integer, BigInteger, String, DateTime, Boolean,ForeignKey,Text,Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

class Auctions(Base):
    __tablename__ = "Auctions"


    AuctionID=Column(Integer, primary_key=True, autoincrement=True)
    SellerUserID=Column(Integer, ForeignKey("Users.UserID"), nullable=True)
    ProductID=Column(Integer, ForeignKey("Products.ProductID"), nullable=False)
    Startdate=Column(DateTime, nullable=True)
    EndDate=Column(DateTime, nullable=True)
    StartingPrice=Column(Float, nullable=True)
    SellerPrice=Column(Float, nullable=True)
    SellerAskedPrice=Column(Float, nullable=True)
    CreateDate=Column(DateTime, nullable=True)
    Status=Column(SmallInteger, nullable=True)

class AuctionDetails(Base):
    __tablename__ = "AuctionDetails"

    AuctionDetailsID=Column(Integer, primary_key=True, autoincrement=True)
    AuctionID=Column(Integer, ForeignKey("Auctions.AuctionID"), nullable=True)
    BidID=Column(Integer, ForeignKey("Bids.BidID"), nullable=True)
    HighestBid=Column(Float, nullable=True)
    CreateDate=Column(DateTime, nullable=True)
    BidStatus=Column(Float, nullable=True)
   
class Bids(Base):
    __tablename__ = "Bids"

    BidID=Column(Integer, primary_key=True, autoincrement=True)
    AuctionID=Column(Integer, ForeignKey("Auctions.AuctionID"), nullable=True)
    UserID=Column(Integer, ForeignKey("Users.UserID"), nullable=True)
    Amount=Column(Float, nullable=True)
    CreateTime=Column(DateTime, nullable=True)

class BidDetails(Base):
    __tablename__ = "BidDetails"

    BidDetailsID=Column(Integer, primary_key=True, autoincrement=True)
    BidID=Column(Integer, ForeignKey("Bids.BidID"), nullable=True)
    Status=Column(Float, nullable=True)
    CreateDate=Column(DateTime, nullable=True)
    