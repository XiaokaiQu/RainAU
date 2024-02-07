from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error_view, name="error"),
    path("initData", views.insert_data, name="InsertData"),
]