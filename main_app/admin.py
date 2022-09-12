from django.contrib import admin
from .models import Recipe, Review, Profile, RecipePhoto

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(RecipePhoto)
