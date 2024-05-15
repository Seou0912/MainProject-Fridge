from django.urls import path
from . import views

app_name = "fridge"

urlpatterns = [
    path("", views.fridge_main, name="fridge-main"),
    path("ingredient/", views.ingredient_create, name="ingredient"),
    path("menu/", views.recommend_menu, name="menu"),
    path("recipe/", views.get_recipe_details, name="recipe"),
]
