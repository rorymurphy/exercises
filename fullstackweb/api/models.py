from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Sequence

from . import Base
class Product(Base):
    __tablename__ = 'product_viewer_product'
    
    id = Column(String, primary_key=True)
    parent_page_url = Column(String)
    merchant_domain = Column(String)
    price = Column(String)
    image_urls = Column(String)
    product_url = Column(String)
    #Having to use a string because SQL Alchemy doesn't like Django's date formats
    last_mod = Column(String)
    visit_id = Column(String)
    visit_status = Column(String)
    page_title = Column(String)
    product_title = Column(String)

    def __init__(self, *args, **kwargs):
        for key in kwargs:
	    setattr(self, key, kwargs[key])
        
    #this would be used to validate a model received via RESTful service before even
    #attempting to write it to the DB. Currently this is a really primitive validation,
    #which would need to be more fleshed out.  In a production system, there would be
    #validation around the format of the id and other fields
    def validate(self):
        #
        valid = (id != None
		 and self.parent_page_url != None
		 and self.merchant_domain != None
		 and self.product_url != None
		 and self.last_mod != None
		 and self.visit_id != None
		 and self.visit_status != None
		 and self.page_title != None
	         and self.product_title != None)
        for img in self.images:
	    valid = valid and img.validate()
	    
	return valid
               
    #It's been more difficult than I would have expected to get Python to JSON serialize
    #things in exactly the format I want.  I doubt this is the cleanest way, but it has
    #been one that has at least given me output in the format I was aiming for.
    def as_dict(self):
        dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        images = []
        for img in self.images:
	    images.append(img.as_dict())
	dict['images'] = images
	return dict

    
class Image(Base):
    __tablename__ = 'product_viewer_image'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    url = Column(String)
    path = Column(String)
    checksum = Column(String)
    product_id = Column(String, ForeignKey('product_viewer_product.id'))
    product = relationship("Product", backref=backref('images', order_by=id))

    #this would be used to validate a model received via RESTful service before even
    #attempting to write it to the DB. Currently this is a really primitive validation,
    #which would need to be more fleshed out.  In a production system, there would be
    #validation around the format of the id and other fields    
    def validate(self):
        return (self.url != None
	    and self.path != None
	    and self.checksum != None
	    and self.product_id != None)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}