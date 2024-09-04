from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import permissions
# Create your views here.


# @api_view(['GET'])
# def getIncome(request):
#     Incomes = Income.objects.all()
#     serializer = IncomeSerializer(Incomes,many=True)
#     return Response(serializer.data)



class Incomelc(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class Incomerud(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'


    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

