from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuctionBase(BaseModel):
    AuctionID:Optional[int]=None
    SellerUserID:Optional[int]=None
    ProductID :Optional[int]=None
    Startdate: Optional[datetime]=None
    EndDate: Optional[datetime]=None
    StartingPrice: Optional[float]=None
    SellerPrice: Optional[float]=None
    SellerAskedPrice: Optional[float]=None
    Status: Optional[int]=None

class AuctionCreate(AuctionBase):
    SellerUserID: Optional[int]=None
    ProductID: Optional[int]=None
    Startdate: Optional[datetime]=None
    EndDate: Optional[datetime]=None
    StartingPrice: Optional[float]=None
    SellerPrice: Optional[float]=None
    SellerAskedPrice: Optional[float]=None
    Status: Optional[int]=None

class AuctionUpdate(AuctionBase):
    AuctionID: Optional[int]=None
    Startdate: Optional[datetime]=None
    EndDate: Optional[datetime]=None
    StartingPrice: Optional[float]=None
    SellerPrice: Optional[float]=None
    SellerAskedPrice: Optional[float]=None
    Status: Optional[int]=None

class BidBase(BaseModel):
    BidID: Optional[int]=None
    AuctionID: Optional[int]=None
    UserID: Optional[int]=None
    Amount: Optional[float]=None

class BidCreate(BidBase):
    AuctionID: Optional[int]=None
    UserID: Optional[int]=None
    Amount: Optional[float]=None