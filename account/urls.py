from django.urls import path

from .views import (
    RegistrationView, ActivationView, LoginView, 
    LogoutView, ChangePasswordView, DropPasswordView, 
    ChangeForgottenPasswordView, UserView
) 



urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('activate/', ActivationView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change password'),
    path('drop-password/', DropPasswordView.as_view(), name='drop_password'),
    path('change-forgotten-password/', ChangeForgottenPasswordView.as_view(), name='change forgotten password'),
    path('users/<int:user_id>/', UserView.as_view(), name='user-detail')
]