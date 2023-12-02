from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_name: str

class CategoryCreate(BaseModel):
    category_name: str
    product_id: int