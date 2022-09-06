from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Recipe, Review, Profile
from .forms import UserForm, ReviewCreate, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

# CLASS-BASED VIEWS
class RecipeCreate(CreateView):
    model = Recipe
    fields = ["name", "description", "cookTime", "totalTime", "ingredients", "instructions"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ["name", "description", "cookTime", "totalTime", "ingredients", "instructions"]
    
    

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