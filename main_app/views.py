from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ingredient, Recipe, Review, Profile, RecipePhoto
from .forms import UserForm, ReviewCreate, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
import os

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# RECIPES
def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/index.html", {"recipes": recipes})

def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    reviews = Review.objects.filter(recipe=recipe_id)
    reviewForm = ReviewCreate()
    favorited = bool
    profile = None
    if request.user.id:
        profile = Profile.objects.get(id = request.user.profile.id)
    if profile:
        if profile.favorites.all().filter(id=recipe_id).exists():
            favorited=True
    else:
        pass
    return render(request, "recipes/detail.html", {"recipe": recipe, "reviewForm": reviewForm, "reviews":reviews, "favorited": favorited})

def reviews_create(request, recipe_id):
    form = ReviewCreate(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.recipe_id = recipe_id
        review.user_id = request.user.id
        review.save()
    return redirect("home")

def add_recipe_photo(request, recipe_id):
        # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind(".") :]
        # just in case something goes wrong
        try:
            bucket = os.environ["S3_BUCKET"]
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            RecipePhoto.objects.create(url=url, recipe_id=recipe_id)
        except Exception as e:
            print("An error occurred uploading files to s3")
            print(e)
    return redirect("recipe_detail", recipe_id=recipe_id)


# CLASS-BASED
class RecipeCreate(CreateView):
    model = Recipe
    fields = ["name", "description", "cookTime", "totalTime", "ingredients", "instructions"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ["name", "description", "cookTime", "totalTime", "ingredients", "instructions"]
    
    

# INGREDIENTS
def ingredients_index(request):
    ingredients = Ingredient.objects.all()
    return render(request, "ingredients/index.html", {"ingredients": ingredients})

def ingredients_detail(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    return render(request, "ingredients/detail.html", {"ingredient":ingredient })


# CLASS-BASED
class IngredientCreate(CreateView):
    model = Ingredient
    fields = ["name", "category"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# PROFILE

def profile_new(request):
    profile_form = ProfileForm()
    return render(request, "profile/profile_new.html", {"profile_form": profile_form})

@login_required
def favorite_add(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    profile = request.user.profile
    if profile.favorites.filter(id=recipe.id).exists():
        profile.favorites.remove(recipe.id)
    else: 
        profile.favorites.add(recipe.id)
    return redirect('recipe_detail', id)

@login_required
def profile_favorites(request):
    profile = Profile.objects.get(user = request.user.id)
    recipes = profile.favorites.all()
    return render(request,"profile/favorites.html", {"profile": profile, "recipes": recipes})


class ProfileCreate(CreateView):
    model = Profile
    fields = ["diet", "about", "age"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def form_invalid(self, form):
        form.instance.user = self.request.user
        form.add_error(None, "Sorry, Something went wrong")
        return super().form_invalid(form)


# Authentication 
def signup(request):
    if request.user.id:
        return redirect('home')
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
    
            user = form.save()
            login(request, user)
            return redirect('profile_create')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)