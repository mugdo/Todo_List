from pyexpat import model
from django.forms import ModelForm
from .models import UserProfileModel

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfileModel

        fields = '__all__'