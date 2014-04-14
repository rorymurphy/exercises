import datetime
from haystack import indexes
from product_viewer.models import Product, Image

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='product_title')
    url = indexes.CharField(model_attr='product_url')
    last_mod = indexes.DateTimeField(model_attr='last_mod')
    
    def get_model(self):
        return Product
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(last_mod__lte=datetime.datetime.now())
