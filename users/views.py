from django.contrib.auth import authenticate
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import CustomRegistrationForm


class RegisterFormView(FormView):
    form_class = CustomRegistrationForm
    template_name = "registration/registration.html"

    def form_valid(self, form):
        form.save()
        data = form.cleaned_data
        authenticate(username=data.get('username'), password=data.get('password'))
        return super(RegisterFormView, self).form_valid(form)

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        host = self.request.get_host()
        if referer:
            referer = referer.split('/')
            referer_host = referer[2]
            if referer_host == host:
                return reverse('main') + '/'.join(referer[3:])
            else:
                return reverse('main')
        else:
            return reverse('main')
