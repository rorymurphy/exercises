import unittest, os, os.path, sys, urllib, json
import tornado.options
from tornado.options import options
from tornado.testing import AsyncHTTPTestCase

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Product, Image
from ..api import ProductListHandler, ProductDetailsHandler, app, start_app, Session, Base

class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestHandlerBase, self).setUp()
        engine = create_engine('sqlite:///')
        Session.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        start_app()
 
    def get_app(self):
        return app # this is the global app that we created above.
 
    def get_http_port(self):
        return options.port

   
#class ApiTests:
class ApiHandlerTest(TestHandlerBase):
    def test_details(self):
      
	expected = {
	    'id': 'df8286fc4a28b14dc86e0b5e63d1bbe9',
	    'parent_page_url': 'http://www.gap.com/browse/category.do?cid=11121',
	    'merchant_domain': 'www.gap.com',
	    'price': '$39.95',
	    'image_urls': 'http://www3.assets-gap.com/webcontent/0005/877/381/cn5877381.jpg',
	    'product_url': 'http://www.gap.com/browse/product.do?cid=64748&vid=1&pid=350338012',
	    'last_mod': '2013-01-23T21:04:39',
	    'visit_id': '0789e70bdec68ffe40ee9ad0691c6b53e3f4e77c',
	    'visit_status': 'new',
	    'page_title': 'GapBody: GapBody: New Arrivals | Gap',
	    'product_title': 'Modal vintage lace gown',
	}
	

	model = Product(**expected)
	session = Session()
        session.add(model)
        session.commit()
	
	response = self.fetch(
	    '/product/df8286fc4a28b14dc86e0b5e63d1bbe9/',
	    method='GET',
	    follow_redirects=False)
	self.assertEqual(response.code, 200)

	actual = json.loads(response.body)
	for key in expected:
	    self.assertEqual( expected[key], actual[key].encode('ascii','ignore') )
    def test_list(self):
	mods = []
	mods.append(Product(**{
	    'id': 'df8286fc4a28b14dc86e0b5e63d1bbe9',
	    'parent_page_url': 'http://www.gap.com/browse/category.do?cid=11121',
	    'merchant_domain': 'www.gap.com',
	    'price': '$39.95',
	    'image_urls': 'http://www3.assets-gap.com/webcontent/0005/877/381/cn5877381.jpg',
	    'product_url': 'http://www.gap.com/browse/product.do?cid=64748&vid=1&pid=350338012',
	    'last_mod': '2013-01-23T21:04:39',
	    'visit_id': '0789e70bdec68ffe40ee9ad0691c6b53e3f4e77c',
	    'visit_status': 'new',
	    'page_title': 'GapBody: GapBody: New Arrivals | Gap',
	    'product_title': 'Modal vintage lace gown',
	}))
	mods.append( Product(**{
	    'id': '515bf618ed92dc16795ac45aee85c69b',
	    'parent_page_url': 'http://www.gap.com/browse/category.do?cid=11121',
	    'merchant_domain': 'www.gap.com',
	    'price': '$19.95',
	    'image_urls': 'http://www3.assets-gap.com/webcontent/0005/631/275/cn5631275.jpg',
	    'product_url': 'http://www.gap.com/browse/product.do?cid=64748&vid=1&pid=321582002',
	    'last_mod': '2013-01-23T21:04:40',
	    'visit_id': '0789e70bdec68ffe40ee9ad0691c6b53e3f4e77c',
	    'visit_status': 'new',
	    'page_title': 'GapBody: GapBody: New Arrivals | Gap',
	    'product_title': 'Modal lace-trim cami',
	}))
	
	session = Session()
	for mod in mods:
	    session.add(mod)
	    
        session.commit()
        
 	response = self.fetch(
	    '/product/',
	    method='GET',
	    follow_redirects=False)
	self.assertEqual(response.code, 200)
	
	actual = json.loads(response.body)
	self.assertEqual( 2, len(actual))