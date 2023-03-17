#from django.conf.urls import url
from django.urls import path, re_path

from .views import TotalUsersChartData
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #url(r'^api/chart/total-users-data/$', TotalUsersChartData.as_view())
    re_path(r'^api/chart/total-users-data/$', TotalUsersChartData.as_view())
]

