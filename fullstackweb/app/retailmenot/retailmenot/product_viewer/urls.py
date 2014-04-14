from django.conf.urls import patterns, url

from product_viewer import views

urlpatterns = patterns('',
    # ex: /product/
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
)