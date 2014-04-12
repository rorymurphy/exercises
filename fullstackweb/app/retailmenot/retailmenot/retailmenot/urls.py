from django.conf.urls import patterns, include, url

from django.contrib import admin
import product_viewer
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'retailmenot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^product/', include('product_viewer.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', include('haystack.urls')),
)
