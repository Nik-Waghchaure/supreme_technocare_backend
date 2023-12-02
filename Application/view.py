from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Application.connection import Base, get_db
from Application.models import Product, Category, SubCategory, SubCategoryDescription , SubCategoryDescriptions
from Application.schemas import ProductCreate, CategoryCreate
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Request

router = APIRouter()


@router.get("/product/")
def get_product_list(db: Session = Depends(get_db)):
    db_product = db.query(Product).all()
    
    if db_product:
        data = jsonable_encoder(db_product)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/product_subcategories/")
async def get_product_subcategories(product_name: str, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_name == product_name).first()
    print(db_product)
    print(db_product.id)
    if db_product:
        db_category = (
            db.query(Category).filter(Category.product_id == db_product.id).all()
        )
        data = jsonable_encoder(db_category)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/category/")
def get_category_list(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()

    result = {}
    for product in all_products:
        sub_categories = (
            db.query(Category).join(Product, Category.product_id == product.id).all()
        )
        sub_category_list = [sub_cat.category_name for sub_cat in sub_categories]
        # return sub_category_list contains sub category name and id 
        sub_cat_list = [ {"id":sub_cat.id, "category_name":sub_cat.category_name} for sub_cat in sub_categories]
        result[product.product_name] = sub_cat_list

    return result


@router.get("/sub_category/{category_name}")
def get_sub_category(category_name: str, db: Session = Depends(get_db)):
    print(category_name,"++++++++++++++++++++++++++++")
    db_category = (
        db.query(Category).filter(Category.category_name == category_name).first()
    )
    print(db_category,"db_category")
    if db_category:
        db_sub_category = (
            db.query(SubCategory)
            .filter(SubCategory.category_id == db_category.id)
            .all()
        )

        data = jsonable_encoder(db_sub_category)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")

@router.post("/sub_category/{category_name_list}")
async def get_sub_category(category_name_list: str, db: Session = Depends(get_db)):
    category_list = []
    if category_name_list:
        print(category_name_list,"++++++++++++++++++++++++++++")
        category_name_list = category_name_list.replace('[','').replace('"',"").replace(']','').replace('%20',' ').split(',')
        print(category_name_list,"++++++++++++++++++++++++++++")

        for category in category_name_list:
            print(category,"category")
            db_category = (
                db.query(SubCategory).filter(SubCategory.sub_category_name == category.replace('"',"")).first()
            )
            print(db_category,"db_category")
            if db_category:
                category_list.append(db_category)
        data = jsonable_encoder(category_list)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")





@router.post("/sub_category_details/{sub_category_name}")
async def get_sub_category_details(
    sub_category_name: str, db: Session = Depends(get_db)
):
    db_sub_category = (
        db.query(SubCategory)
        .filter(SubCategory.sub_category_name == sub_category_name)
        .first()
    )
    if db_sub_category:
        db_sub_category_details = (
            db.query(SubCategoryDescription)
            .filter(SubCategoryDescription.sub_category_id == db_sub_category.id)
            .first()
        )
        data = jsonable_encoder(db_sub_category_details)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)

    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")
    

@router.post("/sub_category_det/{sub_category_name}")
async def get_sub_category_details(
    sub_category_name: str, db: Session = Depends(get_db)
):
    db_sub_category = (
        db.query(SubCategory)
        .filter(SubCategory.sub_category_name == sub_category_name)
        .first()
    )
    print(db_sub_category.id,"db_sub_category")
    if db_sub_category:
        # join query with SubCategory and SubCategoryDescriptions i want SubCategory.sub_category_img in final data output last data
        query = db.query(SubCategory.id,
                         SubCategoryDescriptions.sub_category_id,
                            SubCategory.img_path,
                            SubCategoryDescriptions.sub_category_json,
                            SubCategoryDescriptions.sub_category_json1,
                         ).filter(SubCategoryDescriptions.sub_category_id == db_sub_category.id).join(
                             SubCategory, SubCategoryDescriptions.sub_category_id ==SubCategory.id 
                             ).all()
        print(query[-1])
        query = query[-1]
        data = {
            "sub_category_id":query[0],
            "sub_category_name":sub_category_name,
            "sub_category_img":query[2],
            "sub_category_json":query[3],
            "sub_category_json1":query[4]
        }
        
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        '''
        db_sub_category_details = (
            db.query(SubCategoryDescriptions)
            .filter(SubCategoryDescriptions.sub_category_id == db_sub_category.id)
            .first()
        )
        data = jsonable_encoder(db_sub_category_details)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        '''

    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")
    

