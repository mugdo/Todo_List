from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, PermissionManager
from django.forms import EmailField
from django import forms

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank= True)
    complite = models.BooleanField(default=False)
    create = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complite']


class UserRegistationForm(UserCreationForm):
    email = forms.EmailField()
    # phone = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'password_mismatch': {
                'unique': 'This user is already exist.',
            },
           "password_mismatch": "password error"              
            
        }
class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,related_name='related_profile')
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250,null=True)
    address = models.CharField(max_length=250,null=True)
    blocked = models.BooleanField(default=False)

    image = models.ImageField(null=True, blank=True, upload_to='')
    def __str__(self):
        return self.first_name
    
     

