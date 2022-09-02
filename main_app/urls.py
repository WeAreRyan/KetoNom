from django.urls import path, include
from . import views
# ADDED FOR LOCAL IMAGE FUNCTIONALITY
from django.conf import settings
from django.conf.urls.static import static
# END

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='recipes'),
    path('recipes/create/', views.RecipeCreate.as_view(), name="recipe_create"), 
    path('recipes/<int:recipe_id>/', views.recipes_detail, name="recipe_detail"), 
    path('recipes/<int:recipe_id>/reviews_create', views.reviews_create, name="reviews_create"), 
    path('profile/create/', views.recipes_detail, name="profile_create"), 
    path('accounts/signup/', views.signup, name='signup'),
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)