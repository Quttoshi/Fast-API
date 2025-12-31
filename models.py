from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    quantity: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None        
    price: Optional[float] = None      
    description: Optional[str] = None   
    quantity: Optional[int] = None      

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int