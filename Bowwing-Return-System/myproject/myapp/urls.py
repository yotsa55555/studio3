from django.urls import path
from myapp import views  # Import your views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("registor/", views.registor, name="registor"),
    path("login/", views.user_login, name="login"),
    path("catalog_user/", views.catalog_user, name="catalog_user"),
    path("catalog_staff/", views.catalog_staff, name="catalog_staff"),
    path("catalog_staff/<equipment_id>", views.return_item, name="return_item"),
    path("catalog_admin/", views.catalog_admin, name="catalog_admin"),
    path("user_borrowing/<equipment_id>", views.borrow_view, name="borrow_request"),
    path("home_staff/", views.home_staff, name="home_staff"),
    path("approval_staff/", views.approval_staff, name="approval_staff"),
    path("approval_staff/<borrow_id>", views.borrow_pass, name="borrow_pass"),
    path("history_staff/", views.history_staff, name="history_staff"),
    path("home_user/", views.home_user, name="home_user"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("edit_admin/", views.edit_admin, name="edit_admin"),
    path("home_admin/", views.home_admin, name="home_admin"),
    path("report_admin/", views.report_admin, name="report_admin"),
    path("history_admin/", views.history_admin, name="history_admin"),
    path("edit_admin/<int:equipment_id>/", views.edit_admin, name="edit_admin"),
<<<<<<< HEAD
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<str:token>/", views.reset_password, name="reset_password"),
=======
    path("catalog_admin/<int:equipment_id>/", views.delete_item, name="delete_item"),
    path("add_item/", views.add_item, name="add_item"),
>>>>>>> 4d37d50192df075348887d69b36444bd3702e540
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
