from django.urls import path, re_path

from . import views

app_name = 'rainAU'

urlpatterns = [
    path("", views.main_map, name="mainPage"),
    path("rankRP", views.rank_rain_poss, name="rankRP"),
    re_path(r'^htlocation/(?P<loc>\w+)/$', views.hty_tmp_location, name='htlocation'),
    path("hrPage", views.history_rainfall, name="hrPage"),
    re_path(r'^rainList/(?P<loc>\w+)/$', views.RainInAUListView.as_view(), name='rainList'),
    path("error", views.error_view, name="error"),
    path("initData", views.insert_data, name="InsertData"),
]