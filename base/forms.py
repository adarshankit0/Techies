from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

# forms.py
from django import forms

class GeminiForm(forms.Form):
    input_text = forms.CharField(required=False)
    image_file = forms.ImageField()
