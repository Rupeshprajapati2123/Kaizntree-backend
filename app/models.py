from django.db import models
 
# Create your models here.
class Employee(models.Model):  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    contact = models.CharField(max_length=15) 
   
    class Meta:  
        db_table = "tblemployee"




class Product(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tags = models.JSONField()
    stock_status = models.CharField(max_length=100)
    available_stock = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)  # Add this field
