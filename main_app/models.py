from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date

MEALS = (
    ("B", "Breakfast"),
    ("L", "Lunch"),
    ("D", "Dinner"),
)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    externalLink = models.CharField(max_length=200)
    cookTime = models.IntegerField()
    totalTime = models.IntegerField()
    ingredients = models.CharField(max_length=200)
    instructions = models.TextField()
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    body = models.TextField()
    stars = models.IntegerField(default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)