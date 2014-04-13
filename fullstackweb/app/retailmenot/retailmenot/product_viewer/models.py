from django.db import models
'''
@author: Rory
'''

class Product(models.Model):
    '''
    This is the model for a product - 
    '''
    VISIT_STATUS_NEW = 0
    VISIT_STATUS_CHOICES = (
        (VISIT_STATUS_NEW, 'new'),
    )

    id = models.CharField(max_length = 255, primary_key = True)
    parent_page_url = models.CharField(max_length = 2048)
    merchant_domain = models.CharField(max_length = 255)
    price = models.CharField(max_length = 11)
    image_urls = models.CharField(max_length = 2048)
    product_url = models.CharField(max_length = 2048)
    last_mod = models.DateTimeField()
    visit_id = models.CharField(max_length = 255)
    visit_status = models.IntegerField(choices = VISIT_STATUS_CHOICES, default = VISIT_STATUS_NEW)
    page_title = models.CharField(max_length = 1024)
    product_title = models.CharField(max_length = 255)
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        
    def get_visit_status_text(self):
        return Product.VISIT_STATUS_CHOICES[self.visit_status]
        
class Image(models.Model):
    '''
    classdocs
    '''
    url = models.CharField(max_length = 2048)
    path = models.CharField(max_length = 1024)
    checksum = models.CharField(max_length = 255)
    
    products = models.ManyToManyField(Product, related_name = "images")
    
        