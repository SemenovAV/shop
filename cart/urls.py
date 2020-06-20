from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    re_path('^remove/(?P<product_id>\d+)/$', views.CartRemove.as_view(), name='cart_remove'),
    re_path(r'^add/(?P<product_id>\d+){1}/(?P<url>[/\w+-]+)*/$', views.CartAdd.as_view(), name='cart_add'),



]
