from django.urls import path
from .views import RegisterView, LoginView
from . import views

app_name = 'app_login'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_page, name='logout'),
]