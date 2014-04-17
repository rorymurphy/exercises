import os.path
import json
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.options import define, options, parse_command_line

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Product, Image
from . import Session, Base
define("port", default=8888, help="port to run on", type=int)

#just a marker to indicate this will be created by 
app = None

class ProductListHandler(tornado.web.RequestHandler):
    def get(self):
	session = Session()
	models = session.query(Product).order_by(Product.id)
	result = []
	for mod in models:
	    result.append(mod.as_dict())
	self.set_header('Content-Type', 'application/json')
	self.write(json.dumps(result))
        
    def post(self):
        data = json.loads(self.request.body)
        model = Product(data)
        session = Session()
        session.add(model)
        session.commit()
      

class ProductDetailsHandler(tornado.web.RequestHandler):
    def get(self, prod_id):
        #self.write(prod_id)
        session = Session()
	model = session.query(Product).filter_by(id = prod_id).first()
	if model == None:
	    raise tornado.web.HTTPError(404)
	self.set_header('Content-Type', 'application/json')
	self.write(json.dumps(model.as_dict()))
    
    def update(self):
        self.write('Not Implemented')

def start_app():

    
    app = tornado.web.Application([
            (r"/product/", ProductListHandler),
            (r"/product/([a-f0-9]+)/", ProductDetailsHandler),
    ])
    app.listen(options.port)	

    
if __name__ == "__main__":
    parse_command_line()

    engine = create_engine('sqlite:///app/retailmenot/retailmenot/db.sqlite3')
    Session.configure(bind=engine)
    Base.metadata.bind = engine      
  
    start_app()
    tornado.ioloop.IOLoop.instance().start()