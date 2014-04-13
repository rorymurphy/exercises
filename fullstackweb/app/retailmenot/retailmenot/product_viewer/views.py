from django.template import RequestContext, loader

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django_statsd.clients import statsd

from product_viewer.models import Product, Image

PAGE_SIZE = 20

def index(request):
    prods_by_title = Product.objects.order_by('page_title')
    context = {'products' : prods_by_title}
    statsd.incr('response.200')
    return render(request, 'product_viewer/index.html', context)

def list(request, sort_field = 'page_title', sort_dir = 'desc', page = 0):
    page = int(page)
    prods = Product.objects.order_by(sort_field)
    if sort_dir == 'desc':
        prods = prods.reverse()
    
    page_start = page * PAGE_SIZE
    prods = prods[page_start : page_start + PAGE_SIZE]
    statsd.incr('response.200')
    return HttpResponse(serializers.serialize('json', prods),
                        content_type="application/json")

def detail(request):
    return HttpResponse('stub')
# Create your views here.
