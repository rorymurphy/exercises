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

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from product_viewer.models import Product, Image
from product_viewer.product_serializer import ProductSerializer

PAGE_SIZE = 20

def index(request):
    prods_by_title = Product.objects.order_by('product_title')
    context = {'products' : prods_by_title}
    statsd.incr('response.200')
    return render(request, 'product_viewer/index.html', context)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    #for the purposes of listing, we're going to override the
    #default get_queryset method to check if a 'q' query string
    #parameter has been submitted and, if so, use elasticsearch
    #to get the results
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = None 
        query = self.request.QUERY_PARAMS.get('q', None)
        if query is not None:
            queryset = SearchQuerySet()
            queryset = queryset.filter(content = AutoQuery(query) )
        else:
            queryset = Product.objects.all()
        return queryset
