from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='home'),  # root path goes to register page
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('secret/', views.secret_page, name='secret'),
]
