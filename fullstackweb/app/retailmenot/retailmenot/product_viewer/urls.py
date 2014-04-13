from django.conf.urls import patterns, url

from product_viewer import views

urlpatterns = patterns('',
    # ex: /product/
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^list/(?P<sort_field>\w+)/(?P<sort_dir>asc|desc)/$', views.list, name='list'),
    url(r'^list/(?P<sort_field>\w+)/(?P<sort_dir>asc|desc)/(?P<page>\d+)/$', views.list, name='list'),
    # ex: /product/5/
    #url(r'^(?P<prod_id>\w+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)