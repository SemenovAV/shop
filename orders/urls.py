from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path('ok/', views.OrderOk.as_view(), name='order_ok')
]
