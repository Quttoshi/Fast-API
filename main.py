from fastapi import FastAPI
from models import Product

app = FastAPI()

products = [
    Product(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Product(id=2, name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25)
]

@app.get("/products")
async def get_products(skip: int = 0, limit: int = 10):
    return products[skip : skip + limit]

@app.get("/product/{id}")
async def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "Product not found"

