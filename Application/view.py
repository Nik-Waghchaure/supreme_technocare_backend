from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Application.connection import Base, get_db
from Application.models import Product, Category, SubCategory, SubCategoryDescription, SubCategoryDescriptions, ContactUs
from Application.schemas import ProductCreate, CategoryCreate, ContactForm
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Body, APIRouter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_config = {
    "server": "smtp.hostinger.com",
    "port": 587,
    "username": "inquiry@supremetechnocare.com",
    "password": "Supreme@8177",
}

router = APIRouter()

# For Displaying Drawer Content
@router.get("/category/")
def get_category_list(db: Session = Depends(get_db)):
    all_products = db.query(Product).all()

    result = {}
    for product in all_products:
        sub_categories = db.query(Category).filter(Category.product_id == product.id).all()
        sub_cat_list = [{"id": sub_cat.id, "category_name": sub_cat.category_name} for sub_cat in sub_categories]
        result[product.product_name] = sub_cat_list

    return result

@router.get("/sub_category/{category_name}")
def get_sub_category(category_name: str, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.category_name == category_name).first()
    if db_category:
        db_sub_category = db.query(SubCategory).filter(SubCategory.category_id == db_category.id).all()
        data = jsonable_encoder(db_sub_category)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")

@router.post("/sub_category_det/")
async def get_sub_category_details(request: dict, db: Session = Depends(get_db)):
    product_name = request.get('product_name')
    db_sub_category = db.query(SubCategory).filter(SubCategory.sub_category_name == product_name).first()
    if db_sub_category:
        query = db.query(
            SubCategory.id,
            SubCategory.sub_category_img,
            SubCategoryDescriptions.sub_category_json,
            SubCategoryDescriptions.sub_category_json1,
        ).join(
            SubCategoryDescriptions, SubCategory.id == SubCategoryDescriptions.sub_category_id
        ).filter(
            SubCategoryDescriptions.sub_category_id == db_sub_category.id
        ).all()
        
        if query:
            query = query[-1]
            data = {
                "sub_category_id": query[0],
                "sub_category_name": product_name,
                "sub_category_img": query[1],
                "sub_category_json": query[2],
                "sub_category_json1": query[3]
            }
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=404, detail="Sub Category Details not found")
    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")

@router.post("/contact-us-form/")
async def submit_form(data: dict = Body(...)):
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')
    message = data.get('message')
    enquiries = data.get('enquiries', [])

    try:
        server = smtplib.SMTP(smtp_config["server"], smtp_config["port"])
        server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])

        # Sending email to the user who filled the form
        user_subject = "Thank you for your submission"
        user_body = f"Dear {name},\n\nThank you for submitting the form. We appreciate your interest.\n\nBest regards,\nThe Supreme Technocare Team ⚕️😊"
        user_msg = MIMEMultipart()
        user_msg["From"] = smtp_config["username"]
        user_msg["To"] = email
        user_msg["Subject"] = user_subject
        user_msg.attach(MIMEText(user_body, "plain"))
        server.sendmail(smtp_config["username"], email, user_msg.as_string())

        # Creating the list of enquired items
        enquiry_items = "\n\n".join([f"Sub Category: {item['subCategoryName']}\nImage URL: {item['imageUrl']}" for item in enquiries])

        # Sending email to your own email address
        subject = "New Form Submission"
        body = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nMessage: {message}\n\nEnquired Items:\n{enquiry_items}"
        msg = MIMEMultipart()
        msg["From"] = smtp_config["username"]
        msg["To"] = smtp_config["username"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        server.sendmail(smtp_config["username"], smtp_config["username"], msg.as_string())

        server.quit()

        return JSONResponse(content={"message": "Thanks for Connecting with us..!"})
    except smtplib.SMTPAuthenticationError as auth_error:
        raise HTTPException(status_code=401, detail=f"SMTP Authentication Error: {str(auth_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to Connect! Try again after some time...: {str(e)}")
