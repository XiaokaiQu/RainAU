from django.urls import path, re_path

from . import views

app_name = 'rainAU'

urlpatterns = [
    path("", views.main_map, name="mainPage"),
    path("rankRP", views.rank_rain_poss, name="rankRP"),
    re_path(r'^(?P<pk>\d+)/$', views.hty_tmp_location, name='htlocation'),
    path("error", views.error_view, name="error"),
    path("initData", views.insert_data, name="InsertData"),
]