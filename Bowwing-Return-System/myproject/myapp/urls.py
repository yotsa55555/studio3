from django.urls import path
from myapp import views  # Import your views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("registor/", views.registor, name="registor"),
    path("login/", views.login, name="login"),
    path("catalog_user/", views.catalog_user, name="catalog_user"),
    path("catalog_staff/", views.catalog_staff, name="catalog_staff"),
    path("catalog_admin/", views.catalog_admin, name="catalog_admin"),
    path("user_borrowing/", views.borrow_view, name="borrow_request"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)