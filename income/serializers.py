from rest_framework import serializers
from .models import *

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','incomename','incomebrand','incomecategory','description','price','rating','stock','created_at']
