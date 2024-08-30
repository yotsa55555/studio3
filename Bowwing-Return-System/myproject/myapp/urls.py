from django.urls import path
from myapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registor", views.login, name="registor"),
]
