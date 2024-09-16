from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("records/", views.records, name="records"),
    path("records/edit/<int:pk>/", views.edit_record, name="edit-record"),
]
