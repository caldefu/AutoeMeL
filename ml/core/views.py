from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms


def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {'count':count})


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registratdation/signup.html'

@login_required
def secret(request):
    return render(request, 'secret.html')

class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret2.html'