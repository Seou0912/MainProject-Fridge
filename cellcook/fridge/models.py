from django.db import models
from django.contrib.auth.models import User
from users.models import User

class Ingredient(models.Model):
    ingredient_id = models.CharField(max_length=20, primary_key=True)
    User.id = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=30)
    ingredient_type = models.CharField(max_length=20)
    expiration_date = models.DateTimeField()

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=30)

class IngredientMenuMapping(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    mapping = models.ForeignKey(IngredientMenuMapping, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    description = models.TextField()
    calories = models.FloatField()


