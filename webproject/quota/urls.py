from django.urls import path
from . import views
from webproject.urls import admin

urlpatterns = [
    path("", views.login_view, name="login"),  # Root URL directs to login view
    path("index/", views.index_view, name="index"),  # Separate path for homepage
    path("academic_year/", views.academic_year, name="academic_year"),
    path("course_details/", views.course_details, name="course_details"),
    path("quota_status/", views.quota_status, name="quota_status"),
    path("logout/", views.logout_view, name="logout"),
    path('admin/', admin.site.urls, name = "admin_site")
]
