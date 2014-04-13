from django.template import RequestContext, loader

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django_statsd.clients import statsd
from django.forms import model_to_dict

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from product_viewer.models import Product, Image
from product_viewer.product_serializer import ProductSerializer

PAGE_SIZE = 20

def index(request):
    prods_by_title = Product.objects.order_by('page_title')
    context = {'products' : prods_by_title}
    statsd.incr('response.200')
    return render(request, 'product_viewer/index.html', context)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
