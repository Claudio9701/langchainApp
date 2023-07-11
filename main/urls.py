# Simple Django URL configuration for main app with home view
from django.urls import path
from .views import home, upload_csv_to_analyze, register

urlpatterns = [
    path("", home, name="home"),
    path("upload_csv_to_analyze", upload_csv_to_analyze, name="upload_csv_to_analyze"),
    path("register", register, name="register"),
]
