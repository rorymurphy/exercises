from django.forms import widgets

from rest_framework import pagination
from rest_framework import serializers
from product_viewer.models import Product


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(max_length = 255, required = True)
    parent_page_url = serializers.CharField(max_length = 2048)
    merchant_domain = serializers.CharField(max_length = 255)
    price = serializers.CharField(max_length = 11)
    image_urls = serializers.CharField(max_length = 2048)
    product_url = serializers.CharField(max_length = 2048)
    last_mod = serializers.DateTimeField()
    visit_id = serializers.CharField(max_length = 255)
    visit_status = serializers.IntegerField()
    #visit_status = serializers.CharField(source = 'get_visit_status_text', max_length = 20)
    page_title = serializers.CharField(max_length = 1024)
    product_title = serializers.CharField(max_length = 255)
    images = serializers.RelatedField(many = True)

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.id = attrs.get('id', instance.id)
            instance.parent_page_url = attrs.get('parent_page_url', instance.parent_page_url)
            instance.merchant_domain = attrs.get('linenos', instance.merchant_domain)
            instance.price = attrs.get('price', instance.price)
            instance.image_urls = attrs.get('image_urls', instance.image_urls)
            instance.product_url = attrs.get('image_urls', instance.product_url)
            instance.last_mod = attrs.get('image_urls', instance.last_mod)
            instance.visit_id = attrs.get('image_urls', instance.visit_id)
            instance.visit_status = attrs.get('image_urls', instance.visit_status)
            instance.page_title = attrs.get('image_urls', instance.page_title)
            instance.product_title = attrs.get('image_urls', instance.product_title)
            return instance

        # Create new instance
        return Product(**attrs)

class PaginatedProductSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = ProductSerializer