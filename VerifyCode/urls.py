
from django.urls import path
from VerifyCode import views
urlpatterns = [
    path('login/', views.login),
    path('get_check_code/', views.get_check_code),
    path('register/', views.register),
]