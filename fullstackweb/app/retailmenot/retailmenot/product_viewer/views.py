from django.template import RequestContext, loader

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django_statsd.clients import statsd
from django.forms import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Clean

from product_viewer.models import Product, Image
from product_viewer.product_serializer import ProductSerializer,\
    PaginatedProductSerializer

PAGE_SIZE = 20

def index(request, page=1):
    page = int(page)
    start_idx = (page -1) * PAGE_SIZE
    end_idx = page * PAGE_SIZE
    products = SearchQuerySet().order_by('price')[start_idx:end_idx]
    context = {'page': page, 'products': products }
    return render(request, 'product_viewer/index.html', context)


class ProductList(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
      

    def get_queryset(self):
        """
        for the purposes of listing, we're going to override the
        default get_queryset method to check if a 'q' query string
        parameter has been submitted and use elasticsearch
        to get the results
        """
        queryset = None 
        query = self.request.QUERY_PARAMS.get('q', None)

        queryset = SearchQuerySet()
        if query == None:
            queryset = queryset.order_by('price')
        else:    
            queryset = queryset.filter(content = Clean(query)).order_by('price')

        return queryset
