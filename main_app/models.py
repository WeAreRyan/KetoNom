from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from datetime import date

DIETS = (
    ("None", "No restrictions"),
    ("Keto", "Ketogenic"),
    ("Paleo", "Paleolithic"),
    ("ATK", "Atkins"),
    ("Lo-F", "Low-Fat"),
    ("Raw", "Raw Food"),
    ("LCal", "Low Calorie"),
    ("LCal", "Low Calorie"),
    ("MediT", "Mediterranean"),
    ("DASH", "dietary approaches to stop hypertension"),
    ("Anti-A", "Anti-Inflammatory"),
)

INGREDIENTTYPES = {
    ("U", "unknown"),
    ("M", "Meet"),
    ("P", "Protein"),
    ("V", "Vegetable"),
    ("F", "Fruit"),
    ("H", "Herbs and Spices"),
    ("S", "Starch"),
    ("O", "Oil"),
    ("W", "Sweetener"),
}


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    externalLink = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    cookTime = models.IntegerField()
    totalTime = models.IntegerField()
    ingredients = models.CharField(max_length=200)
    instructions = models.TextField()
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'recipe_id': self.id})

class RecipePhoto(models.Model):
  url = models.CharField(max_length=255)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for recipe_id: {self.recipe_id} @{self.url}"



class Review(models.Model):
    body = models.TextField()
    stars = models.IntegerField(default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    about = models.TextField()
    diet = models.CharField(
        max_length=100, 
        choices=DIETS, 
        default=DIETS[0][0]
        )
    favorites = models.ManyToManyField(Recipe)

    def get_absolute_url(self):
        return reverse('home')

class Ingredient(models.Model):
    name = models.Charfield(max_length=50)
    type = models.CharField(
        max_length=10, 
        choices=INGREDIENTTYPES, 
        default=INGREDIENTTYPES[0][0])
    def __str__(self):
        return self.name