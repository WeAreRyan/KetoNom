from django.contrib import admin
from .models import Recipe, Review, Profile, RecipePhoto, Ingredient

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(RecipePhoto)
admin.site.register(Ingredient)
