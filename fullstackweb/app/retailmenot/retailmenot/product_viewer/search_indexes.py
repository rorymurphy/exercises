import datetime
from haystack import indexes
from product_viewer.models import Product, Image

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    id = indexes.CharField(model_attr='id')
    product_title = indexes.CharField(model_attr='product_title')
    product_url = indexes.CharField(model_attr='product_url')
    last_mod = indexes.DateTimeField(model_attr='last_mod')
    
    parent_page_url = indexes.CharField(model_attr='parent_page_url')
    merchant_domain = indexes.CharField(model_attr='merchant_domain')
    price = indexes.CharField(model_attr='price')
    image_urls = indexes.CharField(model_attr='image_urls')
    page_title = indexes.CharField(model_attr='page_title')

  
    def get_model(self):
        return Product
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(last_mod__lte=datetime.datetime.now())
