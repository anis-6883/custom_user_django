from django.contrib import admin
from django.urls import path ,include
from app_login.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('app_login.urls')),
    path('', HomeView.as_view(), name='home'),
]
