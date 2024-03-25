from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Application.connection import Base, get_db
from Application.models import Product, Category, SubCategory, SubCategoryDescription , SubCategoryDescriptions, ContactUs
from Application.schemas import ProductCreate, CategoryCreate, ContactForm
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Request

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import Body


smtp_config = {
    "server": "smtp.hostinger.com",
    "port": 487,
    "username": "inquiry@supremetechnocare.com",
    "password": "Supreme@8177",
}


# FastMail instance
# fast_mail = FastMail(mail_config)



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

# @router.post("/sub_category/{category_name_list}")
# async def get_sub_category(category_name_list: str, db: Session = Depends(get_db)):
#     category_list = []
#     if category_name_list:
#         print(category_name_list,"++++++++++++++++++++++++++++")
#         category_name_list = category_name_list.replace('[','').replace('"',"").replace(']','').replace('%20',' ').split(',')
#         print(category_name_list,"++++++++++++++++++++++++++++")

#         for category in category_name_list:
#             print(category,"category")
#             db_category = (
#                 db.query(SubCategory).filter(SubCategory.sub_category_name == category.replace('"',"")).first()
#             )
#             print(db_category,"db_category")
#             if db_category:
#                 category_list.append(db_category)
#         data = jsonable_encoder(category_list)
#         return JSONResponse(content=data, status_code=status.HTTP_200_OK)
#     else:
#         raise HTTPException(status_code=404, detail="Sub Category not found")





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
    

# @router.post("/sub_category_det/")
# async def get_sub_category_details(
#     request : dict, db: Session = Depends(get_db)
# ):
#     print(request.get('product_name'),"sub_category_name")
#     product_name = request.get('product_name')
#     db_sub_category = (
#         db.query(SubCategory)
#         .filter(SubCategory.sub_category_name == product_name)
#         .first()
#     )
#     print(db_sub_category.id,"db_sub_category")
#     if db_sub_category:
#         # join query with SubCategory and SubCategoryDescriptions i want SubCategory.sub_category_img in final data output last data
#         query = db.query(SubCategory.id,
#                          SubCategoryDescriptions.sub_category_id,
#                             SubCategory.img_path,
#                             SubCategoryDescriptions.sub_category_json,
#                             SubCategoryDescriptions.sub_category_json1,
#                          ).filter(SubCategoryDescriptions.sub_category_id == db_sub_category.id).join(
#                              SubCategory, SubCategoryDescriptions.sub_category_id ==SubCategory.id 
#                              ).all()
#         print(query[-1])
#         query = query[-1]
#         data = {
#             "sub_category_id":query[0],
#             "sub_category_name":product_name,
#             "sub_category_img":query[2],
#             "sub_category_json":query[3],
#             "sub_category_json1":query[4]
#         }
        
#         return JSONResponse(content=data, status_code=status.HTTP_200_OK)
#         '''
#         db_sub_category_details = (
#             db.query(SubCategoryDescriptions)
#             .filter(SubCategoryDescriptions.sub_category_id == db_sub_category.id)
#             .first()
#         )
#         data = jsonable_encoder(db_sub_category_details)
#         return JSONResponse(content=data, status_code=status.HTTP_200_OK)
#         '''

#     else:
#         raise HTTPException(status_code=404, detail="Sub Category not found")
    



@router.post("/sub_category_det/")
async def get_sub_category_details(
    request: dict, db: Session = Depends(get_db)
):
    print(request.get('product_name'), "sub_category_name")
    product_name = request.get('product_name')
    db_sub_category = (
        db.query(SubCategory)
        .filter(SubCategory.sub_category_name == product_name)
        .first()
    )
    print(db_sub_category.id, "db_sub_category")
    if db_sub_category:
        # Fetching the sub-category details along with the image URL from SubCategoryDescriptions
        query = db.query(SubCategory.id,
                         SubCategoryDescriptions.sub_category_id,
                         SubCategory.img_path,
                         SubCategoryDescriptions.sub_category_json,
                         SubCategoryDescriptions.sub_category_json1,
                         SubCategoryDescriptions.sub_category_header1  # Add this line
                         ).filter(SubCategoryDescriptions.sub_category_id == db_sub_category.id).join(
            SubCategory, SubCategoryDescriptions.sub_category_id == SubCategory.id
        ).all()
        print(query[-1])
        query = query[-1]
        data = {
            "sub_category_id": query[0],
            "sub_category_name": product_name,
            "sub_category_img": query[2],
            "sub_category_json": query[3],
            "sub_category_json1": query[4],
            "sub_category_header1_img": query[5]  # Add this line
        }

        return JSONResponse(content=data, status_code=status.HTTP_200_OK)

    else:
        raise HTTPException(status_code=404, detail="Sub Category not found")




# @router.post("/submit-form")
# async def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)): 
#     print(f"Name: {name}, Email: {email}, Message: {message}")
 
#     try:
#         server = smtplib.SMTP(smtp_config["server"], smtp_config["port"])
#         server.starttls()
#         server.login(smtp_config["username"], smtp_config["password"])

#         subject = "New Form Submission"
#         body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

#         msg = MIMEMultipart()
#         msg["From"] = smtp_config["username"]
#         msg["To"] = "insanem371@gmail.com"
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "plain"))

#         server.sendmail(smtp_config["username"], "inquiry@supremetechnocare.com", msg.as_string())

#         server.quit()

#         return JSONResponse(content={"message": "Email sent successfully"})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    




    
    
@router.post("/contact-us-formmm/")
async def submit_form(contact_form: ContactForm,db: Session = Depends(get_db)):
    # print("AGHVHV")
    try:
       
        server = smtplib.SMTP(smtp_config["server"], smtp_config["port"])
        server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])

        subject = "New Form Submission"
        body = f"Name: {contact_form.name}\nEmail: {contact_form.email}\nMessage: {contact_form.message}"

        msg = MIMEMultipart()
        msg["From"] = smtp_config["username"]
        msg["To"] = "insanem371@gmail.com"
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(smtp_config["username"], "inquiry@supremetechnocare.com", msg.as_string())

        server.quit()
        db_contact = ContactUs(
            name=contact_form.name,
            email=contact_form.email,
            mobile=contact_form.mobile,
            message=contact_form.message
        )

        # Add to session and commit to database
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        db.close()

        return JSONResponse(content={"message": "Email sent successfully"})
    except smtplib.SMTPAuthenticationError as auth_error:
        raise HTTPException(status_code=401, detail=f"SMTP Authentication Error: {str(auth_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")






# @router.post("/contact-us-form/")
# # async def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
# # async def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
# async def submit_form(data: dict = Body(...)):
#     name = data.get('name')
#     email = data.get('email')
#     message = data.get('message')
#     try:
#         server = smtplib.SMTP('smtp.hostinger.com', 587)  # Hostinger SMTP server and port
#         server.starttls()
#         server.login('inquiry@supremetechnocare.com', 'Supreme@8177')  # Your Hostinger email credentials

#         subject = "New Form Submission"
#         body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

#         msg = MIMEMultipart()
#         msg["From"] = 'inquiry@supremetechnocare.com'  # Your email address
#         msg["To"] = "insanem371@gmail.com"  # Recipient's email address
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "plain"))

#         server.sendmail('inquiry@supremetechnocare.com', "insanem371@gmail.com", msg.as_string())

#         server.quit()

#         return JSONResponse(content={"message": "Email sent successfully"})
#     except smtplib.SMTPAuthenticationError as auth_error:
#         raise HTTPException(status_code=401, detail=f"SMTP Authentication Error: {str(auth_error)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@router.post("/contact-us-form/")
async def submit_form(data: dict = Body(...)):
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')
    message = data.get('message')
    try:
        server = smtplib.SMTP('smtp.hostinger.com', 587)  # Hostinger SMTP server and port
        server.starttls()
        server.login('inquiry@supremetechnocare.com', 'Supreme@8177')  # Your Hostinger email credentials

        # Sending email to the user who filled the form
        user_subject = "Thank you for your submission"
        user_body = f"Dear {name},\n\nThank you for submitting the form. We appreciate your interest.\n\nBest regards,\nThe Supreme Technocare Team ⚕️😊"

        user_msg = MIMEMultipart()
        user_msg["From"] = 'inquiry@supremetechnocare.com'  # Your email address
        user_msg["To"] = email  # User's email address
        user_msg["Subject"] = user_subject
        user_msg.attach(MIMEText(user_body, "plain"))

        server.sendmail('inquiry@supremetechnocare.com', email, user_msg.as_string())

        # Sending email to your own email address
        subject = "New Form Submission"
        body = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nMessage: {message}"

        msg = MIMEMultipart()
        msg["From"] = 'inquiry@supremetechnocare.com'  # Your email address
        msg["To"] = "inquiry@supremetechnocare.com"  # Your email address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail('inquiry@supremetechnocare.com', "inquiry@supremetechnocare.com", msg.as_string())

        server.quit()

        return JSONResponse(content={"message": "Thanks for Connecting with us..!"})
    except smtplib.SMTPAuthenticationError as auth_error:
        raise HTTPException(status_code=401, detail=f"SMTP Authentication Error: {str(auth_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to Connect! \n Try again after some time...: {str(e)}")
