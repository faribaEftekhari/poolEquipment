from django.db import models
from django.contrib.auth.models import User
from accounts import models as accountmodel
# Create your models here.
class pomps(models.Model):
    brand=models.CharField(max_length=70)
    modelnum=models.CharField(max_length=70)
    price=models.PositiveIntegerField(default=0)
    madein=models.CharField(max_length=70)
    slug=models.SlugField()
    discription=models.TextField(null=True)
    image=models.ImageField(default='default.jpg',blank=True)
    author=models.ForeignKey(User,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return self.brand

    def snippet(self):
        return self.discription[:50]+ '  ...'
class order(models.Model):
    customer=models.ForeignKey(accountmodel.Customer,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('pomps',on_delete=models.CASCADE,null=True)
    orderdate=models.DateField(auto_now_add=True,null=True)
    quantity=models.PositiveIntegerField(default=1)
    totalprice=models.PositiveIntegerField(default=0)
