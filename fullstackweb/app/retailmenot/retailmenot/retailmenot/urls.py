from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework import viewsets, routers

from product_viewer import views
#import product_viewer
admin.autodiscover()

#Django REST API Routing
#class ProductViewSet(viewsets.ModelViewSet):
#    model = product_viewer.models.Product
    
#router = routers.DefaultRouter()
#router.register(r'products', ProductViewSet)
#End Django REST API

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'retailmenot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'product_viewer.views.index', name='index'),
    url(r'^product/$', views.ProductList.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^search/', include('haystack.urls')),
)
