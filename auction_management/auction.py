# product_management/product.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from sqlalchemy_orm.auction_models import Auctions,Bids
from sqlalchemy_orm.models import Products
from sqlalchemy_orm.db_config import SessionLocal
from .auction_schema import AuctionCreate, AuctionUpdate, BidCreate  # Import schema
from datetime import datetime
from utils import return_payload

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_auction")
async def create_auction(auction: AuctionCreate, db: Session = Depends(get_db)):
    try:
        product=db.query(Products).filter(Products.ProductID==auction.ProductID).first()
        if not product:
            return return_payload(404,message="No product found.")
        if product.IsAuction==True:
            return return_payload(400, message="Product already in auction, please update auction status")
        if auction.EndDate<=datetime.utcnow():
            return return_payload(400,message="End time must be in the future")

        new_auction=Auctions(
            SellerUserID=auction.SellerUserID,
            ProductID=auction.ProductID,
            Startdate=auction.Startdate,
            EndDate=auction.EndDate,
            StartingPrice=auction.StartingPrice,
            SellerPrice=auction.SellerPrice,
            SellerAskedPrice=auction.SellerAskedPrice,
            Status=auction.Status
        )

        db.add(new_auction)
        db.commit()
        db.refresh(new_auction)

        return return_payload(200,message="Auction Added Successfully.")
    except Exception as e:
        return return_payload(500, message="Error: "+str(e))

@router.put("/edit_auction")
async def edit_auction(auction: AuctionUpdate, db: Session = Depends(get_db)):
    try:
        db_auction=db.query(Auctions).filter(Auctions.AuctionID==auction.AuctionID).first()
        if not db_auction:
            return return_payload(404,message="Auction Not found.")
        
        db_auction.Startdate=auction.Startdate if auction.Startdate!=None else db_auction.Startdate
        db_auction.EndDate=auction.EndDate if auction.EndDate!=None else db_auction.EndDate
        db_auction.StartingPrice=auction.StartingPrice if (auction.StartingPrice!=None and auction.StartingPrice==0) else db_auction.StartingPrice
        db_auction.SellerPrice=auction.SellerPrice if (auction.SellerPrice!=None and auction.SellerPrice==0) else db_auction.SellerPrice
        db_auction.Status=auction.Status if auction.Status!=None  else db_auction.Status

        db.commit()
        db.refresh(db_auction)

        return return_payload(200,message="Auction Updated.")

    except Exception as e:
        return return_payload(500, message="Error: "+str(e))
    

# Place Bid Endpoint
@router.post("/place_bid")
async def place_bid(bid: BidCreate, db: Session = Depends(get_db)):
    try:
        db_auction = db.query(Auctions).filter(Auctions.AuctionID == bid.AuctionID).first()
        if not db_auction:
            return return_payload(404, message="Auction not found")

        # Validate auction timing
        if db_auction.EndDate < datetime.utcnow():
            return return_payload(400, message="Auction has ended")

        # Validate bid amount
        if bid.Amount < db_auction.StartingPrice:
            return return_payload(400, message="Bid amount is less than the starting price")

        highest_bid = (
            db.query(Bids)
            .filter(Bids.AuctionID == bid.AuctionID)
            .order_by(Bids.Amount.desc())
            .first()
        )
        if highest_bid and bid.Amount <= highest_bid.Amount:
            return return_payload(400, message="Bid amount must be higher than the current highest bid")

        # Create new bid
        new_bid = Bids(
            AuctionID=bid.AuctionID,
            UserID=bid.UserID,
            Amount=bid.Amount,
            CreateTime=datetime.utcnow()
        )
        db.add(new_bid)
        db.commit()
        db.refresh(new_bid)

        return return_payload(200,message="Bid placed successfully")
    except Exception as e:
        return return_payload(500, message="Error: "+str(e))
    
@router.post("/view_auction_and_bids")
async def view_auction_and_bids(AuctionID:int,db: Session = Depends(get_db)):
    try:
        auction_details=db.query(Auctions).filter(Auctions.AuctionID==AuctionID).first()
        if not auction_details:
            return return_payload(404,message="No Auction found")
        
        bids=db.query(Bids).filter(Bids.AuctionID==AuctionID).order_by(Bids.Amount.desc())
        payload={
            "Auction":auction_details,
            "Bids": bids
        }
        return return_payload(200,message="Get Auction details successfully",payload=payload)
    except Exception as e:
        return return_payload(500, message="Error: "+str(e))