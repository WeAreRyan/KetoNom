from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ReviewCreate
from .models import Recipe, Review, Profile
from .forms import UserForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/index.html", {"recipes": recipes})

def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    reviews = Review.objects.filter(recipe=recipe_id)
    reviewForm = ReviewCreate()
    return render(request, "recipes/detail.html", {"recipe": recipe, "reviewForm": reviewForm, "reviews":reviews })

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
    fields = ["name", "cookTime", "totalTime", "ingredients", "instructions"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileCreate(CreateView):
    model = Profile
    fields = ["diet", "about"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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