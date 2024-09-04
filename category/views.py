from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import permissions
# Create your views here.


# @api_view(['GET'])
# def getproduct(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products,many=True)
#     return Response(serializer.data)



class Productlc(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class Productrud(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = '_id'


    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)




def my_custom_page_not_found_view(request,exception):
    return render(request,'404_not_found.html')


def my_custom_server_error_view(request):
    return render(request,'server_error.html')