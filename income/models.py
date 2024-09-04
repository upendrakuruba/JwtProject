from django.db import models
from users.models import *
# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    incomename = models.CharField(max_length=255)
    incomebrand = models.CharField(max_length=255,null=True,blank=True)
    incomecategory = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=255)
    rating =models.DecimalField( max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True,editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user)+'s income'
    