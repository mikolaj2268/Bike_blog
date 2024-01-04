from . import views
from django.urls import path
from .views import UserRegisterView
from .views import forgot_password, ForgotPasswordView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]
