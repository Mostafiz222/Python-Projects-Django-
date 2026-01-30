from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.
def about(request):
    context={'page':'about'}
    return render(request ,"about.html",context)
@login_required(login_url="/login/")
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
@login_required(login_url="/login/")
def delete_recipe(request,id):
    queryset=Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/recipe/')

@login_required(login_url="/login/")
def update_recipe(request,slug):
    queryset=Recipe.objects.get(slug = slug)
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
def login_page(request):
        if request.method == "POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
    
            if  not User.objects.filter(username = username).exists():
                messages.error(request,'Invalid Username')
                return redirect("/login/")
            user=authenticate(username=username,password=password)
            if user is None:
                messages.error(request,"Invalid Password")
                return redirect("/login/")
            else:
                login(request,user)
                return redirect("/recipe/")
        return render(request,'login.html')

def register(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user =User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"Username already taken")
            return redirect ('/register/')
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()
        messages.info(request,"Account created successfully")
        return redirect("/register/")
    
    return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
    
from django.db.models import Q,Sum
from .seed import generate_report_card
def get_students(request):
    queryset=Student.objects.all()
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-Student_age')
    for rank in ranks:
        print(rank.marks)

    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(Student_name__icontains= search)|
            Q(department__department__icontains= search)
         )
    paginator = Paginator(queryset, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    return render(request,'report/students.html',{'queryset':page_obj})

def seemarks(request,student_id):
    generate_report_card()
    queryset=SubjectMarks.objects.filter(student__StudentID__studentid=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))

    cur_rank=-1
    i=1
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-Student_age')
    for rank in ranks:
        if student_id == rank.StudentID.studentid:
             cur_rank=i
             break
        i=i+1

    return render (request,'report/seemarks.html',{'queryset':queryset,'total_marks':total_marks,'cur_rank':cur_rank})