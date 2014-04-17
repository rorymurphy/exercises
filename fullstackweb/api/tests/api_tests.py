import unittest, os, os.path, sys, urllib
import tornado.options
from tornado.options import options
from tornado.testing import AsyncHTTPTestCase

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Product, Image
from ..api import ProductListHandler, ProductDetailsHandler, app

Session = sessionmaker()
Base = declarative_base()

class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestHandlerBase, self).setUp()
        engine = create_engine('sqlite:///app/retailmenot/retailmenot/db.sqlite3')
        Session.configure(bind=engine)
        Base.metadata.bind = engine
 
    def get_app(self):
        return app # this is the global app that we created above.
 
    def get_http_port(self):
        return options.port

   
#class ApiTests:
class ApiHandlerTest(TestHandlerBase):
    def test_details(self):
	expected = Product({
	    id: 'df8286fc4a28b14dc86e0b5e63d1bbe9',
	    'parent_page_url': 'http://www.gap.com/browse/category.do?cid=1112',
	    'merchant_domain': 'www.gap.com',
	    'price': '$39.95',
	    'image_urls': 'http://www3.assets-gap.com/webcontent/0005/877/381/cn5877381.jpg',
	    'product_url': 'http://www.gap.com/browse/product.do?cid=64748&vid=1&pid=35033801',
	    'last_mod': '2013-01-23T21:04:39',
	    'visit_id': '0789e70bdec68ffe40ee9ad0691c6b53e3f4e77',
	    'visit_status': 'new',
	    'page_title': 'GapBody: GapBody: New Arrivals | Gap',
	    'product_title': 'Modal vintage lace gown',
	})
	
	response = self.fetch(
	    '/df8286fc4a28b14dc86e0b5e63d1bbe9/',
	    method='GET',
	    follow_redirects=False)
	self.assertEqual(response.code, 200)
	
	
	for c in expected.__table__.columns:
	    self.assertEqual( getattr(expected, c.name), getattr(actual, c.name) )