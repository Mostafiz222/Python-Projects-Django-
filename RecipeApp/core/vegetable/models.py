from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_name=models.CharField(max_length=100)
    recipe_description=models.CharField()
    recipe_image=models.ImageField(upload_to="recipe")
