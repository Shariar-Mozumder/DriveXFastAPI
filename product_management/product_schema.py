from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    UserID: int
    CategoryID: int
    Name: str
    Description: Optional[str] = None
    Specifications: Optional[str] = None
    Price : float
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

class ProductUpdate(ProductBase):
    UserID: Optional[int] = None
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

class CategoryBase(BaseModel):
    categoryName: str
    categoryType: Optional[str] = None
    status: Optional[int] = None

class CategoryCreate(CategoryBase):
    categoryName: str
    categoryType: Optional[str] = None
    status: Optional[int] = None