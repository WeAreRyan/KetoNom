from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DIETS

from main_app.models import Review, Profile

# DIET = (
#     ("None", "No restrictions"),
#     ("Keto", "Ketogenic"),
#     ("Paleo", "Paleolithic"),
#     ("ATK", "Atkins"),
#     ("Lo-F", "Low-Fat"),
#     ("Raw", "Raw Food"),
#     ("LCal", "Low Calorie"),
#     ("LCal", "Low Calorie"),
#     ("MediT", "Mediterranean"),
#     ("DASH", "dietary approaches to stop hypertension"),
#     ("Anti-A", "Anti-Inflammatory"),
# )

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password1' ,'password2' )

class ReviewCreate(ModelForm): 
    class Meta:
        model = Review
        fields = ["body", "stars"]

class ProfileForm(forms.Form):
    # class Meta: 
    #     model = Profile
    #     fields = ["age", "about", "diet"]


    age = forms.IntegerField()
    about = forms.CharField()
    diet = forms.MultipleChoiceField(choices = DIETS)