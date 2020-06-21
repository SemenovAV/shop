from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import CustomRegistrationForm, CustomAuthForm


class RegisterFormView(FormView):
    form_class = CustomRegistrationForm
    template_name = "registration/registration.html"
    referer = None

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get('HTTP_REFERER')
        return super(RegisterFormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        data = form.cleaned_data
        username = data['email']
        password = data['password2']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        host = self.request.get_host()
        if self.referer:
            referer = self.referer.split('/')
            referer_host = referer[2]
            if referer_host == host:
                return reverse('main') + '/'.join(referer[3:])
            else:
                return reverse('main')
        else:
            return reverse('main')


class CustomUserLoginForm(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthForm

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)
        return super(CustomUserLoginForm, self).form_valid(form)
