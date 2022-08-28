from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Recipe, Review
from .forms import UserForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def recipes_index(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/index.html", {"recipes": recipes})







def signup(request):
    if request.user.id:
        return redirect('home')
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
    
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)