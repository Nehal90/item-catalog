import os

import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(750))

class Category(Base):
    __tablename__ = 'category'

    cid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    categoryItems = relationship("CategoryItem", cascade = "all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category-name': self.name,
            'category-id': self.cid,
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'

    name = Column(String(80), nullable=False)
    item_id = Column(Integer, primary_key=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.cid'))
    created_on = Column(DateTime, default=func.now())
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category-id': self.category_id,  
            'item-id': self.item_id,
            'item-name': self.name,
            'item-description': self.description,
        }
         

engine = create_engine('sqlite:///catelogitemswithusers.db')

# engine = create_engine('postgres://uiqzqtqlesjzzn:fxAK1ml3_UGwN9YOz70-Y_L66-@ec2-107-20-242-191.compute-1.amazonaws.com:5432/dv91n1mvr0bap')

Base.metadata.create_all(engine)




