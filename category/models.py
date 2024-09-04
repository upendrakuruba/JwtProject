from django.db import models
from users.models import *
# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    productname = models.CharField(max_length=255)
    # image = models.ImageField(upload_to='media')
    productbrand = models.CharField(max_length=255,null=True,blank=True)
    productcategory = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=255)
    rating =models.DecimalField( max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True,editable=False)


    def __str__(self):
        return self.productname
    