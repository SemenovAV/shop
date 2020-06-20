from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'(?P<absolute_url>[/\w+-]+)*/$', views.StoreFrontView.as_view(), name='catalog'),
]
