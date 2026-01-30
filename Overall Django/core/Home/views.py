from django.shortcuts import render, redirect
from django.http import HttpResponse
from vegetable.seed import *
from .utils import send_email_to_client,send_email_with_attachment
from django.conf import settings

def home(request):
    seed_db()

def send_mail(request):
    subject="this is from django server"
    message="hey"
    recipent_list=["..@gmail.com"]
    file_path=f"{settings.BASE_DIR}/hello.html"
    send_email_with_attachment(subject,message,recipent_list,file_path)
    return redirect('/')
    
