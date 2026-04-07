from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.db.crud.product import ProductCrud
from app.db.scheme.products import ProductCreate, ProductUpdate

class ProductService:
    async def create_product_service(db: AsyncSession, product_data: ProductCreate):
        return await ProductCrud.create_product(db, product_data)


    async def get_all_products_service(db: AsyncSession):
        return await ProductCrud.get_all_products(db)


    async def get_product_by_id_service(db: AsyncSession, product_id: int):
        db_product = ProductCrud.get_product_by_id(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return await db_product


    async def update_product_service(db: AsyncSession, product_id: int, product_data: ProductUpdate):
        db_product = await ProductCrud.get_product_by_id(db, product_id)

        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        return await ProductCrud.update_product(db, db_product, product_data)


    async def delete_product_service(db: AsyncSession, product_id: int):
        db_product = ProductCrud.get_product_by_id(db, product_id)

        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        ProductCrud.delete_product(db, db_product)
        return {"msg": "삭제 성공"} 