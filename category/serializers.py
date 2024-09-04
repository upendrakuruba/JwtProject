from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['_id','productname','productbrand','productcategory','description','price','rating','stock','created_at']
