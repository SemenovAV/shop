from django.contrib.auth import views
from django.urls import path

from users.forms import CustomAuthForm
from users.views import RegisterFormView, CustomUserLoginForm

urlpatterns = [
    path('login/', CustomUserLoginForm.as_view(
        template_name="registration/login.html",
        form_class=CustomAuthForm
    ),
         name='login'
         ),
    path('registration/', RegisterFormView.as_view(), name='registration'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
