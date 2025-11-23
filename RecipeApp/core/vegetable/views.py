from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
# Create your views here.
def about(request):
    context={'page':'about'}
    return render(request ,"about.html",context)
def recipe(request):
    if(request.method=="POST"):

        data=request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        Recipe.objects.create(
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            recipe_image=recipe_image,
        
        )
        return redirect('/recipe/')
    queryset=Recipe.objects.all()
    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains = request.GET.get('search'))

    context={'recipe':queryset}  
    
    return render(request,'recipe.html',context)

def delete_recipe(request,id):
    queryset=Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/recipe/')


def update_recipe(request,id):
    queryset=Recipe.objects.get(id = id)
    if request.method == "POST":
        data =request.POST
        recipe_name=data.get('recipe_name')
        recipe_description=data.get('recipe_description')
        recipe_image=request.FILES.get('recipe_image')
        
        queryset.recipe_name=recipe_name
        queryset.recipe_description=recipe_description
        #if queryset.recipe_image:
        queryset.recipe_image=recipe_image
        
        queryset.save()
        return redirect('/recipe/')
    
    context={'recipe':queryset}
    return render(request,'update_recipe.html',context)
