from fastapi import APIRouter, HTTPException, Depends, Query
from models import Product, ProductCreate, ProductUpdate
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

products_db: List[Product] = [
    Product(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Product(id=2, name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25)
]

async def validate_pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)) -> dict:
    """Validate pagination parameters with defaults"""
    return {"skip": skip, "limit": limit}


@router.get("")  
async def list_products(pagination: dict = Depends(validate_pagination)) -> List[Product]:
    skip = pagination["skip"]
    limit = pagination["limit"]
    return products_db[skip : skip + limit]


@router.get("/{product_id}")  
async def get_product(product_id: int) -> Product:
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product {product_id} not found")


@router.post("", status_code=201)  
async def create_product(product_data: ProductCreate) -> Product:
    new_id = max([p.id for p in products_db]) + 1 if products_db else 1
    
    new_product = Product(
        id=new_id,
        name=product_data.name,
        price=product_data.price,
        description=product_data.description,
        quantity=product_data.quantity
    )
    products_db.append(new_product)
    return new_product


@router.put("/{product_id}")  
async def update_product(product_id: int, product_data: ProductUpdate) -> Product:
    product = None
    for p in products_db:
        if p.id == product_id:
            product = p
            break
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.quantity is not None:
        product.quantity = product_data.quantity
    
    return product


@router.delete("/{product_id}", status_code=204) 
async def delete_product(product_id: int) -> None:
    global products_db
    initial_length = len(products_db)
    products_db = [p for p in products_db if p.id != product_id]
    
    if len(products_db) == initial_length:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    return None

@router.get("/jokes/random")
async def get_random_joke():
    """Fetch a random joke from external API"""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=503, detail="External API failed")
