from django.urls import path, include
from . import views 

# ADDED FOR LOCAL IMAGE FUNCTIONALITY
from django.conf import settings
from django.conf.urls.static import static
# END

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('recipes/', views.recipes_index, name='recipes_index'),
    path('recipes/create/', views.RecipeCreate.as_view(), name="recipe_create"), 
    path('recipes/<int:recipe_id>/', views.recipes_detail, name="recipe_detail"), 
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name="recipe_update"), 
    path('recipes/<int:recipe_id>/reviews_create', views.reviews_create, name="reviews_create"), 
    path('recipes/<int:recipe_id>/add_photo/', views.add_recipe_photo, name='add_recipe_photo'),
    path('profile/create/', views.ProfileCreate.as_view(), name="profile_create"), 
    path('profile/new/', views.profile_new, name="profile_new"), 
    path('favorite/<int:id>/', views.favorite_add, name="favorite_add"), 
    path('favorites/', views.profile_favorites, name="profile_favorites"), 
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)