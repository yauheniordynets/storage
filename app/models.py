from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    alternative_name = Column(String(255))
    quantity = Column(Float)
    quantity_in_metres = Column(Integer)
    status = Column(Boolean)


class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    row_number = Column(Integer)
    column_number = Column(Integer)

    product = relationship('Product', back_populates='positions')
    Product.positions = relationship('Position', back_populates='product')
