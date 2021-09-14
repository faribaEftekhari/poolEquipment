from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    isseller=models.BooleanField(default=False)
    isbuyer=models.BooleanField(default=False)
    mobile=models.CharField(max_length=20,null=False)
    address=models.CharField(max_length=40)
    image=models.ImageField(default='default.jpg',upload_to='profile_pic/',null=True,blank=True)
    @property
    def get_name(self):
        return self.user.first_name +' '+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
