from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework import viewsets, routers

from product_viewer import views
#import product_viewer
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'product_viewer.views.index', name='index'),
    url(r'^page/(?P<page>\d+)/$', 'product_viewer.views.index', name='index'),
    url(r'^product/$', views.ProductList.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
