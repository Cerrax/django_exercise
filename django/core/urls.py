from django.urls import path

from core import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', views.LogoutView.as_view(), name = 'logout'),
]