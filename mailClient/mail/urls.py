from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('sendmail/', views.send_email, name="sendmail"),
    path('sent/', views.sent, name="sent"),
]