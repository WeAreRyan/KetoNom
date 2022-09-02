from django.contrib.auth.models import User
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

# class RecipePhoto(models.Model):
#     recipe_image = models.ImageField(null=True, blank=True, upload_to="images/")



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
    about = models.TextField()
    diet = models.CharField(
        max_length=100, 
        choices=DIETS, 
        default=DIETS[0][0]
        )
    favorites = models.ManyToManyField(Recipe)
