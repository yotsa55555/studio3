from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")


def login(request):
    return render(request, "login.html")

def registor(request):
    return render(request, "registor.html")

def catalog_user(request):
    return render(request, "catalog_user.html")

def borrow_view(request):
    return render(request, "borrow_user.html")
