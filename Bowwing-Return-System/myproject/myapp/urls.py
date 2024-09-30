from django.contrib import admin
from django.urls import path, include
from myapp import views  # Import your views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("registor/", views.registor, name="registor"),
    path("login/", views.login, name="login"),
    path("catalog_user/", views.catalog_user, name="catalog_user"),
    path("user_borrowing/", views.borrow_view, name="borrow_request"),
]
