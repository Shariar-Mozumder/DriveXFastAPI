# product_management/product.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy_orm.models import Categories,Users,Products
from sqlalchemy_orm.db_config import SessionLocal
from .product_schema import ProductCreate, ProductUpdate, CategoryCreate  # Import schema
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

# Add product Category

@router.post("/add_category")
async def add_category(category: CategoryCreate,db: Session = Depends(get_db)):
    #check if same category available or not
    try:
        cat=db.query(Categories).filter(Categories.CategoryName.lower() == category.categoryName.lower())
        if not cat:
            new_cat=Categories(
                CategoryName=category.categoryName,
                CategoryType=category.categoryType,
                CreateDate=datetime.utcnow(),
                Status=1
            )
            db.add(new_cat)
            db.commit()
            db.refresh(new_cat)
            return return_payload(200,message="Category created successfully.")
        else:
            return_payload(400,message="Category already exist.")
    except Exception as e:
        return_payload(500,message="Error: "+str(e))

# Add Product Endpoint
@router.post("/add_product")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        # Check if category exists
        category = db.query(Categories).filter(Categories.CategoryID == product.CategoryID).first()
        if not category:
            return return_payload(400, message="Category not found")

        # Check if user is authorized (seller)
        user = db.query(Users).filter(Users.UserID == product.UserID).first()
        if not user:
            return return_payload(400, message="Seller not found")

        # Create new product
        new_product = Products(
            UserID= product.UserID,
            CategoryID=product.CategoryID,
            Name=product.Name,
            Description=product.Description,
            Specifications=product.Specifications,
            Price=product.Price,
            Quantity=product.Quantity,
            IsAuction=product.IsAuction,
            Status=product.Status,
            CreatedDate=datetime.utcnow(),
            CreatedBy=product.UserID
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return return_payload(200,message="Product Added Successfully.",payload={"Name: "+new_product.Name})
    except Exception as e:
        return return_payload(500,message="Error"+str(e))