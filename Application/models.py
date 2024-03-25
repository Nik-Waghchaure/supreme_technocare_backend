from Application.connection import Base
from sqlalchemy import JSON, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    is_delete = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP)
    updatedate = Column(TIMESTAMP)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    category_name = Column(String)
    is_delete = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP)
    updatedate = Column(TIMESTAMP)


class SubCategory(Base):
    __tablename__ = "sub_category"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    sub_category_name = Column(String)
    sub_category_img = Column(String)
    img_path = Column(String)
    is_delete = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP)
    updatedate = Column(TIMESTAMP)
    

class SubCategoryDescription(Base):
    __tablename__ = "sub_category_description"

    id = Column(Integer, primary_key=True, index=True)
    sub_category_id = Column(Integer, ForeignKey("sub_category.id"))
    sub_category_header = Column(String)
    sub_category_json = Column(JSON)
    sub_category_header1 = Column(String)
    sub_category_json1 = Column(JSON)
    sub_category_header2 = Column(String)
    sub_category_json2 = Column(JSON)
    sub_category_header3 = Column(String)
    sub_category_json3 = Column(JSON)
    sub_category_header4 = Column(String)
    sub_category_json4 = Column(JSON)
    sub_category_header5 = Column(String)
    sub_category_json5 = Column(JSON)
    sub_category_header6 = Column(String)
    sub_category_json6 = Column(JSON)
    sub_category_header7 = Column(String)
    sub_category_json7 = Column(JSON)
    sub_category_header8 = Column(String)
    sub_category_json8 = Column(JSON)
    sub_category_header9 = Column(String)
    sub_category_json9 = Column(JSON)
    sub_category_header10 = Column(String)
    sub_category_json10 = Column(JSON)
    is_delete = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updatedate = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

class SubCategoryDescriptions(Base):
    __tablename__ = 'sub_category_des'

    id = Column(Integer, primary_key=True, index=True)
    sub_category_id = Column(Integer, ForeignKey('sub_category.id'))  # Assuming 'sub_category' is the parent table
    sub_category_header = Column(String, nullable=False)
    sub_category_json = Column(JSON, nullable=False)
    sub_category_header1 = Column(String)
    sub_category_json1 = Column(JSON)
    url = Column(String, nullable=False)
    is_delete = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updatedate = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


class ContactUs(Base):
    __tablename__ = "contactus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    message = Column(String)
    createdAt = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    updatedate = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')