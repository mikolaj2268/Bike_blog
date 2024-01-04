from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ForgotPasswordView(TemplateView):
    template_name = 'forgot_password.html'

def forgot_password(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            message = f'Email would be sent to: {user.email}'
            # Here, you would normally add logic to send an email
        except User.DoesNotExist:
            message = 'There is no user with that username in our database.'

    return render(request, 'forgot_password.html', {'message': message})


