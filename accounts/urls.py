from django.urls import include, path
from . import views
from rest_framework import routers

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('forgot-password/', views.ForgotPassword.as_view()),
    path('user/valid', views.isUserValid),
    path('admin/valid', views.isAdminValid)
]