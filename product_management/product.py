# product_management/product.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from sqlalchemy_orm.models import Categories,Users,Products,Images
from sqlalchemy_orm.db_config import SessionLocal
from .product_schema import ProductCreate, ProductUpdate, CategoryCreate, ProductFilter,UpdateImage  # Import schema
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
        cat=db.query(Categories).filter(Categories.CategoryName == category.categoryName).first()
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
            return return_payload(400,message="Category already exist.")
    except Exception as e:
        return return_payload(500,message="Error: "+str(e))

@router.get("/get_all_categories")
async def getAllCategories(db: Session = Depends(get_db)):
    try:
        categories=db.query(Categories).all()
        if len(categories)>0:
            return return_payload(200,message="Get all categories successfully.",payload=categories)
        else:
            return return_payload(200,message="No Category found.")
    except Exception as e:
        return return_payload(500,message="Error: "+str(e))


# Add Product Endpoint
@router.post("/add_product")
async def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        with db.begin():
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
            # db.commit()
            # db.refresh(new_product)
            db.flush()

            imgs=Images(
                ProductID=new_product.ProductID,
                ImageFile1=product.imagefile1,
                ImageFile2=product.imagefile2,
                ImageFile3=product.imagefile3,
                ImageFile4=product.imagefile4,
                ImageFile5=product.imagefile5

            )

            db.add(imgs)
            # db.commit()
            # db.refresh(imgs)

        return return_payload(200,message="Product Added Successfully.",payload={"Name: "+new_product.Name})
    except Exception as e:
        return return_payload(500,message="Error"+str(e))
    
    
@router.post("/get_all_Products_filter")
async def getAllProducts(Productfilters: ProductFilter, db: Session = Depends(get_db)):
    try:

        # Start with the base query
        query = db.query(Products)

    
         # Collect filter conditions
        conditions = []
        if Productfilters.SearchString!=None and Productfilters.SearchString !="":
            conditions.append(Products.Name.like(f"%{Productfilters.SearchString}%"))
        if Productfilters.SearchString!=None and Productfilters.SearchString !="":
            conditions.append(Products.Description.like(f"%{Productfilters.SearchString}%"))

        # Apply AND/OR logic
        if conditions:
            query = query.filter(or_(*conditions))

        # Apply filters if provided
        if Productfilters.CategoryID!=None and Productfilters.CategoryID>0:
            query = query.filter(Products.CategoryID==Productfilters.CategoryID)  # Case-sensitive
        if (Productfilters.UpperPriceRange!=None and Productfilters.UpperPriceRange >0) and (Productfilters.LowerPriceRange==None or Productfilters.LowerPriceRange==0):
            query = query.filter(Products.Price<=Productfilters.UpperPriceRange)
        if (Productfilters.LowerPriceRange!=None and Productfilters.LowerPriceRange>0) and (Productfilters.UpperPriceRange==None or Productfilters.UpperPriceRange==0):
            query = query.filter(Products.Price>=Productfilters.LowerPriceRange)
        if (Productfilters.UpperPriceRange!=None and Productfilters.LowerPriceRange!=None) and  Productfilters.UpperPriceRange>0 and Productfilters.LowerPriceRange>0:
            priceconditions = []
            priceconditions.append(Products.Price<=Productfilters.UpperPriceRange)
            priceconditions.append(Products.Price>=Productfilters.LowerPriceRange)
            query = query.filter(and_(*priceconditions))

        # Execute the query
        products = query.all()


        #add the images
        productwithimgs=[]
        if len(products)>0:
            for product in products:
                imgs=db.query(Images).filter(Images.ProductID==product.ProductID).first()
                payload={"ProductData":product,"Images":imgs}
                productwithimgs.append(payload)
            return return_payload(200,message="Get all products successfully.",payload=productwithimgs)
        else:
            return return_payload(200,message="No Products found.")
    except Exception as e:
        return return_payload(500,message="Error: "+str(e))
    
@router.get("/view_all_products")
async def view_all(db: Session = Depends(get_db)):
    try:
        products=db.query(Products).all()
        #add the images
        productwithimgs=[]
        if len(products)>0:
            for product in products:
                imgs=db.query(Images).filter(Images.ProductID==product.ProductID).first()
                payload={"ProductData":product,"Images":imgs}
                productwithimgs.append(payload)
            return return_payload(200,message="Get all products successfully.",payload=productwithimgs)
        else:
            return return_payload(200,message="No Products available")
        
    except Exception as e:
        return return_payload(500,message="Error:"+str(e))
    
@router.post("/update_product")
async def update_product(update:ProductUpdate,db: Session = Depends(get_db)):
    try:
        product=db.query(Products).filter(Products.ProductID==update.ProductID).first()
        if not product:
            return return_payload(404,message="Product Not found.")
        
        product.CategoryID=update.CategoryID if (update.CategoryID!=None and update.CategoryID!=0) else product.CategoryID
        product.Name=update.Name if (update.Name!=None and update.Name!="") else product.Name
        product.Description=update.Description if (update.Description!=None and update.Description!="") else product.Description
        product.Specifications=update.Specifications if (update.Specifications!=None and update.Specifications!="") else product.Specifications
        product.Price= update.Price if (update.Price!=None and update.Price!=0) else product.Price
        product.Quantity=update.Quantity if (update.Quantity!=None and update.Quantity!=0) else product.Quantity
        product.IsAuction=update.IsAuction if (update.IsAuction!=None) else product.IsAuction
        product.Status=update.Status if (update.Status!=None) else product.Status

        db.commit()
        db.refresh(product)
        # db.flush()

        return return_payload(200,message="Product Updated.", payload={"Name: "+product.Name})
    
    except Exception as e:
        return return_payload(500,message="Error:"+str(e))
    
@router.post("/get_product_by_id")
async def get_product_by_id(ProductID:int, db: Session = Depends(get_db)):
    try:
        product=db.query(Products).filter(Products.ProductID==ProductID).first()
        if product:
            imgs=db.query(Images).filter(Images.ProductID==product.ProductID).first()
            payload={"ProductData":product,"Images":imgs}
            return return_payload(200,message="Get all products successfully.",payload=payload)
        else:
            return return_payload(200,message="No Products available")
        
    except Exception as e:
        return return_payload(500,message="Error:"+str(e))
    
@router.post("/update_product_images")
async def update_product_images(images:UpdateImage,db: Session = Depends(get_db)):
    try:
        img=db.query(Images).filter(Images.ProductID==images.ProductID).first()
        if img:
            img.ImageFile1=images.imagefile1 if (images.imagefile1!=None and images.imagefile1!="") else img.ImageFile1
            img.ImageFile2=images.imagefile2 if (images.imagefile2!=None and images.imagefile2!="") else img.ImageFile2
            img.ImageFile3=images.imagefile3 if (images.imagefile3!=None and images.imagefile3!="") else img.ImageFile3
            img.ImageFile4=images.imagefile4 if (images.imagefile4!=None and images.imagefile4!="") else img.ImageFile4
            img.ImageFile5=images.imagefile5 if (images.imagefile5!=None and images.imagefile5!="") else img.ImageFile5

            db.commit()
            db.refresh(img)

            return return_payload(200,message="Image updated successfully.")
        else:
            imgs=Images(
                ProductID=images.ProductID,
                ImageFile1=images.imagefile1,
                ImageFile2=images.imagefile2,
                ImageFile3=images.imagefile3,
                ImageFile4=images.imagefile4,
                ImageFile5=images.imagefile5

            )

            db.add(imgs)
            db.commit()
            db.refresh(imgs)

            return return_payload(200,message="Image added successfully.")

    except Exception as e:
        return return_payload(500,message="Error:"+str(e))

    

