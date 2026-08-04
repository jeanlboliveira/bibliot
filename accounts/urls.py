from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import register_view, profile_view, adicionar_endereco_view


app_name = 'accounts'

urlpatterns = [
    path("register/", register_view, name='register' ),
    path("profile/", profile_view, name="profile"),
    path("enderecos/adicionar/", adicionar_endereco_view, name='adicionar_endereco'),

    path("login/", auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm,
        next_page = 'core:home'
    ), name='login'),
    
    path("logout/", auth_views.LogoutView.as_view(
        next_page='core:home'
    ), name='logout'),

]
