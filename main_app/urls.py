from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='recipes'),
    path('recipes/create/', views.RecipeCreate.as_view(), name="recipe_create"), 
    path('accounts/signup/', views.signup, name='signup'),
]