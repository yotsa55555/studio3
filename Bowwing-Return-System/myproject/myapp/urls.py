from django.urls import path
from myapp import views  # Import your views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("registor/", views.registor, name="registor"),
    path("login/", views.login, name="login"),
    path("catalog_user/", views.catalog_user, name="catalog_user"),
    path("catalog_staff/", views.catalog_staff, name="catalog_staff"),
    path("catalog_admin/", views.catalog_admin, name="catalog_admin"),
    path("user_borrowing/<equipment_id>", views.borrow_view, name="borrow_request"),
    path("home_staff/", views.home_staff, name="home_staff"),
    path("approval_staff/", views.approval_staff, name="approval_staff"),
    path("history_staff/", views.history_staff, name="history_staff"),
    path("home_user/", views.home_user, name="home_user"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("edit_admin/", views.edit_admin, name="edit_admin"),
    path("home_admin/", views.home_admin, name="home_admin"),
    path("report_admin/", views.report_admin, name="report_admin"),
    path("history_admin/", views.history_admin, name="history_admin"),
    path("edit_admin/<int:equipment_id>/", views.edit_admin, name="edit_admin"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
