"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from users.forms import CustomAuthForm
from django.urls import path, re_path
from storefront.views import MainView, CartView, StoreFrontView
from users.views import RegisterFormView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=CustomAuthForm),
         name='login'
         ),
    path('registration/', RegisterFormView.as_view(), name='registration'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', MainView.as_view(), name='main'),
    path('cart/', CartView.as_view(), name='cart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

urlpatterns += [re_path('[a-z0-9-_]+', StoreFrontView.as_view(), name='by_category'), ]
