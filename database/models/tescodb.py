from sqlalchemy import Integer, String, Float, Text, JSON, Column

from database.conection import DeclarativeBase


class TescoDB(DeclarativeBase):
    __tablename__ = "tesco_base"

    id = Column(Integer, primary_key=True)
    product_url = Column('product_url', String(500))  # str
    product_id = Column('product_id', Integer())  # int
    image_url = Column('image_url', String(500))  # str
    product_title = Column('product_title', String(200))  # str
    category = Column('category', String(200))  # str
    price = Column('price', Float())  # float
    product_description = Column('product_description', Text())  # str
    name_and_address = Column('name_and_address', Text())  # str
    return_address = Column('return_address', Text())  # str
    net_contents = Column('net_contents', Text())  # str
    review = Column('review',
                    JSON())  # list: Review Title (str),Stars Count (int), Author (str), Date (str),Review Text (str)
    usually_bought_next_products = Column('usually_bought_next_products',
                                          JSON())  # list: Product URL(str), Product Title(str)
