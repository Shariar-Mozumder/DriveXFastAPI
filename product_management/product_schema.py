from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    ProductID:Optional[int]=None
    UserID: Optional[int]=None
    CategoryID: Optional[int]=None
    Name: Optional[str]=None
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    Price : Optional[float]=None
    Quantity : Optional[int] = 1
    IsAuction: Optional[bool] = False
    Status: Optional[int] = 1

class ProductCreate(ProductBase):
    UserID: int
    CategoryID: int
    Name: str
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    Price : float
    Quantity : Optional[int] = 1
    IsAuction: Optional[bool] = False
    Status: Optional[int] = 1
    imagefile1: Optional[str] = None
    imagefile2: Optional[str] = None
    imagefile3: Optional[str] = None
    imagefile4: Optional[str] = None
    imagefile5: Optional[str] = None

class ProductUpdate(ProductBase):
    ProductID:Optional[int]=None
    CategoryID: Optional[int] = None
    Name: Optional[str] = None
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    Price : Optional[float] = None
    Quantity : Optional[int] = None
    IsAuction: Optional[bool] = None
    Status: Optional[int] = None

class ProductResponse(ProductBase):
    UserID: Optional[int] = None
    CategoryID: Optional[int] = None
    Name: Optional[str] = None
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    Price : Optional[float] = None
    Quantity : Optional[int] = None
    IsAuction: Optional[bool] = None
    Status: Optional[int] = None

class ProductFilter(ProductBase):
    UserID: Optional[int] = None
    CategoryID: Optional[int] = None
    Name: Optional[str] = None
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    UpperPriceRange : Optional[float] = 0
    LowerPriceRange : Optional[float] = 0
    IsAuction: Optional[bool] = None
    Status: Optional[int] = None
    SearchString: Optional[str] = None

class CategoryBase(BaseModel):
    categoryName: str
    categoryType: Optional[str] = None
    status: Optional[int] = None

class CategoryCreate(CategoryBase):
    categoryName: str
    categoryType: Optional[str] = None
    status: Optional[int] = None

class UpdateImage(BaseModel):
    ProductID:Optional[int]=None
    imagefile1: Optional[str] = None
    imagefile2: Optional[str] = None
    imagefile3: Optional[str] = None
    imagefile4: Optional[str] = None
    imagefile5: Optional[str] = None