from django.urls import path

from . import views

app_name = 'rainAU'

urlpatterns = [
    path("", views.main_map, name="mainPage"),
    path("rankRP", views.rank_rain_poss, name="rankRP"),
    path("error", views.error_view, name="error"),
    path("initData", views.insert_data, name="InsertData"),
]