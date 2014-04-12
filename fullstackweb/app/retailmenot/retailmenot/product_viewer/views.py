from django.template import RequestContext, loader

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django_statsd.clients import statsd

from product_viewer.models import Product, Image

def index(request):
    prods_by_title = Product.objects.order_by('page_title')
    context = {'products' : prods_by_title}
    statsd.incr('response.200')
    return render(request, 'product_viewer/index.html', context)

def list(request):
    prods_by_title = Product.objects.order_by('page_title')
    statsd.incr('response.200')
    return HttpResponse(serializers.serialize('json', prods_by_title),
                        content_type="application/json")

def detail(request):
    return HttpResponse('stub')
# Create your views here.
